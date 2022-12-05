export async function getCoordinates (apiKey: string, address: string): Promise<[string, string]> {
  address = `Северодвинск, ${address}`
  const url = `https://geocode-maps.yandex.ru/1.x/?geocode=${address}&lang=ru_RU&result=1&apikey=${apiKey}&format=json`
  const response = await (await fetch(url)).json()
  if (!('response' in response)) throw new Error(response)
  return response.response.GeoObjectCollection.featureMember[0].GeoObject.Point.pos.split(' ')
}
