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

api.get('/wakatime', (c) => {
  return c.json({
    "type": "event"
  })
})

export const config = {
  runtime: 'edge'
}
export default handle(app)
