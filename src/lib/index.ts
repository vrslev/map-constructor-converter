import { getCoordinates } from './api'
import { featureCollectionSchema } from './geojson'
import { convertGeojsonToRoutes } from './geojson-to-routes'
import { dumpRoutes, parseRoutes } from './routes'
import { convertRoutesToGeojson } from './routes-to-geojson'

export async function toGeojson (routes: string, apiKey: string): Promise<string> {
  const geojson = await convertRoutesToGeojson(
    parseRoutes(routes), async (address) => await getCoordinates(apiKey, address)
  )
  return JSON.stringify(geojson)
}

export function fromGeojson (geojson: string): string {
  const obj = featureCollectionSchema.parse(JSON.parse(geojson))
  const routes = convertGeojsonToRoutes(obj)
  return dumpRoutes(routes)
}

export function getOutputPath (): string {
  return Date.now().toLocaleString()
}
