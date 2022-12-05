import { z } from 'zod'

const addressSchema = z.object({
  description: z.string(),
  // planUrl: z.string().url()
  planUrl: z.string()
})

type PersonName = string
type TypeOfChecking = string
export type Address = typeof addressSchema['_output']

export interface Routes { [k: PersonName]: { [k: TypeOfChecking]: Address[] } }

export function parseRoutes (content: string): Routes {
  const result: Routes = {}
  let curName: PersonName | null = null
  let curType: TypeOfChecking | null = null
  let curRoutes: Address[] = []
  let throwNextLine = false
  const lines = content.split(/\r\n|(?!\r\n)[\n-\r\x85\u2028\u2029]/)

  function saveRoutes (): void {
    if (curName != null && curType != null && curRoutes.length !== 0) {
      result[curName][curType] = curRoutes
      curType = null
      curRoutes = []
    } else {
      if (curName != null) {
        throw new Error(curName)
      }
      if (curType != null) {
        throw new Error(curType)
      }
      if (curRoutes.length !== 0) {
        throw new Error(curRoutes.toString())
      }
    }
  }

  lines.forEach((line, idx) => {
    line = line.trim()

    if (line === '') {
      saveRoutes()
      curName = null
    } else if (line.endsWith(':')) {
      line = line.slice(undefined, -1)

      if (curName != null) {
        if (curType != null) saveRoutes()
        curType = line
      } else {
        curName = line
        result[curName] ??= {}
      }
    } else {
      if (!throwNextLine) {
        const address: Address = {
          description: line.replace(/^(Ситилинк, )/, '').trim(),
          planUrl: lines[idx + 1]
        }
        curRoutes.push(addressSchema.parse(address))
      }
      throwNextLine = !throwNextLine
    }
  })

  saveRoutes()
  return result
}

export function dumpRoutes (routes: Routes): string {
  let lines: string[] = []

  for (const [personName, personRoutes] of Object.entries(routes)) {
    let personLines = [`${personName}:`]

    for (const [typeOfChecking, addresses] of Object.entries(personRoutes)) {
      const personRoutesLines = [`${typeOfChecking}:`]

      for (const address of addresses) {
        personRoutesLines.push(`Ситилинк, ${address.description}`)
        personRoutesLines.push(address.planUrl)
      }

      personLines = personLines.concat(personRoutesLines)
    }

    lines = lines.concat(personLines)
    lines.push('')
  }

  return lines.join('\n')
}

if (import.meta.vitest != null) {
  const desc = (count: number): string => `addr ${count}`
  const url = (count: number): string => `https://example.com/${count}`
  const address = (count: number): Address => ({ description: desc(count), planUrl: url(count) })
  const content = `\
Иван Иванов:
Подключения:
${desc(1)}\r\n${url(1)}
${desc(2)}\r\n${url(2)}
Ремонты:
Ситилинк, ${desc(3)}\r\n${url(3)}

Петров:
Подключения:
Ситилинк, ${desc(4)}\n${url(4)}
`
  const cleanContent = `\
Иван Иванов:
Подключения:
Ситилинк, ${desc(1)}
${url(1)}
Ситилинк, ${desc(2)}
${url(2)}
Ремонты:
Ситилинк, ${desc(3)}
${url(3)}

Петров:
Подключения:
Ситилинк, ${desc(4)}
${url(4)}
`
  const routes: Routes = {
    'Иван Иванов': {
      Подключения: [
        address(1), address(2)
      ],
      Ремонты: [
        address(3)
      ]
    },
    Петров: {
      Подключения: [
        address(4)
      ]
    }
  }

  test('parseRoutes', () => {
    expect(parseRoutes(content)).toStrictEqual(routes)
  })

  test('dumpRoutes', () => {
    expect(dumpRoutes(routes)).toEqual(cleanContent)
  })
}
