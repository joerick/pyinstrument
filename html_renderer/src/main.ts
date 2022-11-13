import './app.css'
import App from './App.svelte'
import type { SessionData } from './lib/dataTypes'
import Session from './lib/model/Session'

export default {
  render(element: HTMLElement, data: SessionData) {
    const session = new Session(data)

    return new App({
      target: element,
      props: { session },
    })
  }
}
