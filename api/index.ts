import { Hono } from 'hono'
import { handle } from 'hono/vercel'
import { inject } from "@vercel/analytics"
import { injectSpeedInsights } from '@vercel/speed-insights';

injectSpeedInsights();

const app = new Hono()
const api = app.basePath('/api')

app.get('/', (c) => {
  return c.json({ message: 'Index!' })
})

api.get('/', (c) => {
  return c.json({ message: 'Hello Hono!' })
})

export const config = {
  runtime: 'edge'
}
export default handle(app)
