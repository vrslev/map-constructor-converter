import { Feature, FeatureCollection } from './geojson'
import { Address, type Routes } from './routes'

// https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
function shuffle<T> (array: T[]): T[] {
  let currentIndex = array.length
  let randomIndex
  while (currentIndex !== 0) {
    randomIndex = Math.floor(Math.random() * currentIndex)
    currentIndex--;
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]]
  }
  return array
}

function * cycle<T> (array: T[]): Generator<T, void, undefined> {
  while (true) yield * array
}

function * getColorGenerator (): Generator<string, void, undefined> {
  const colors = shuffle([
    '#93cbfa',
    '#4996f7',
    '#3a79c3',
    '#204675',
    '#f8d44e',
    '#f0983f',
    '#d87c36',
    '#db534b',
    '#7cd859',
    '#51aa31',
    '#99a131',
    '#595959',
    '#b3b3b3',
    '#e378cd',
    '#a62ff6',
    '#71401a'
  ])
  yield * cycle(colors)
}

function buildTypeOfChecking (type: string): string {
  type = type.toLowerCase()
  switch (type) {
    case 'ремонт':
    case 'ремонты':
      return 'Р'
    case 'подключение':
    case 'подключения':
      return 'П'
    default:
      return type
  }
}

function buildCaption (personName: string, typeOfChecking: string, addressDescription: string): string {
  const [, ...lastNameParts] = personName.split(' ')
  // eslint-disable-next-line @typescript-eslint/strict-boolean-expressions
  const lastName = lastNameParts.join(' ') || personName
  const apartment = addressDescription.split(' ').pop()
  if (apartment === undefined) throw new Error('no apartment')
  const type = buildTypeOfChecking(typeOfChecking)
  return `${lastName} ${type} ${apartment}`
}

function getOffsetter (): (lat: number, lon: number) => [number, number] {
  const latOffsets: { [k: number]: number } = {}
  const lonOffsets: { [k: number]: number } = {}
  const offset = 0.00005

  return (lat, lon) => {
    latOffsets[lat] ??= 0
    lonOffsets[lon] ??= 0

    if (latOffsets[lat] <= lonOffsets[lon]) {
      latOffsets[lat] += 1
    } else {
      lonOffsets[lon] += 1
    }

    return [
      (lat + latOffsets[lat] * offset - offset),
      (lon + lonOffsets[lon] * offset - offset)
    ]
  }
}

type GetCoordinates = (address: string) => Promise<[string, string]>

async function buildFeature (
  id: number,
  address: Address,
  personName: string,
  typeOfChecking: string,
  color: string,
  getCoordinates: GetCoordinates,
  offsetCoordinates: ReturnType<typeof getOffsetter>
): Promise<Feature> {
  const [origLat, origLon] = await getCoordinates(address.description)
  const coordinates = offsetCoordinates(parseFloat(origLat), parseFloat(origLon))
  const description = `${address.description} \n${address.planUrl}`
  const iconCaption = buildCaption(personName, typeOfChecking, address.description)
  return {
    type: 'Feature',
    id,
    geometry: { type: 'Point', coordinates },
    properties: { description, iconCaption, 'marker-color': color }
  }
}

export async function convertRoutesToGeojson (routes: Routes, getCoordinates: GetCoordinates): Promise<FeatureCollection> {
  const offsetCoordinates = getOffsetter()
  const colorGenerator = getColorGenerator()
  const promises: Array<Promise<Feature>> = []
  let id = 0

  for (const [personName, personRoutes] of Object.entries(routes)) {
    const color = colorGenerator.next().value
    if (color == null) throw new Error('no color')

    for (const [typeOfChecking, addresses] of Object.entries(personRoutes)) {
      for (const address of addresses) {
        const feature = buildFeature(id, address, personName, typeOfChecking, color, getCoordinates, offsetCoordinates)
        promises.push(feature)
        id += 1
      }
    }
  }

  const features = await Promise.all(promises)
  return { type: 'FeatureCollection', features }
}

if (import.meta.vitest != null) {
  test.each([
    ['Иван Иванов', 'Подключения', 'Первомайская, 1, 10', 'Иванов П 10'],
    ['Иван Иванов', 'Подключение', 'Первомайская, 1, 10', 'Иванов П 10'],
    ['Иванов', 'Ремонты', 'Первомайская, 1, 0', 'Иванов Р 0'],
    ['Иванов', 'Ремонт', 'Первомайская, 1, 0', 'Иванов Р 0'],
    ['Иванов', 'Другое', 'Первомайская, 1, 0', 'Иванов другое 0']
  ])('convertRoutesToGeojson', (personName, typeOfChecking, addressDescription, result) => {
    expect(buildCaption(personName, typeOfChecking, addressDescription)).toEqual(result)
  })
}
