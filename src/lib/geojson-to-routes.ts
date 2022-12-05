import { FeatureCollection } from './geojson'
import { Address, Routes } from './routes'

function getTypeOfChecking (type: string): string {
  switch (type) {
    case 'Р':
      return 'Ремонты'
    case 'П':
      return 'Подключения'
    default:
      return type.toUpperCase()
  }
}

export function convertGeojsonToRoutes (collection: FeatureCollection): Routes {
  const result: Routes = {}

  for (const feature of collection.features) {
    const [description, planUrl] = feature.properties.description.split(' \n')
    const address: Address = { description, planUrl }
    const [lastName, type] = feature.properties.iconCaption.split(' ')
    const typeOfChecking = getTypeOfChecking(type)

    result[lastName] ??= {}
    result[lastName][typeOfChecking] ??= []
    result[lastName][typeOfChecking].push(address)
  }

  return result
}
