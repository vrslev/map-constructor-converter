import { z } from 'zod'

const pointSchema = z.object({
  type: z.literal('Point'),
  coordinates: z.tuple([z.number(), z.number()])
})

const propertiesSchema = z.object({
  description: z.string(),
  iconCaption: z.string(),
  'marker-color': z.string()
})

const featureSchema = z.object({
  type: z.literal('Feature'),
  id: z.number(),
  geometry: pointSchema,
  properties: propertiesSchema
})

export type Feature = typeof featureSchema['_output']

export const featureCollectionSchema = z.object({
  type: z.literal('FeatureCollection'),
  features: z.array(featureSchema)
})

export type FeatureCollection = typeof featureCollectionSchema['_output']
