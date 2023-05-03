import * as algokit from '@algorandfoundation/algokit-utils'
import { AppSpec } from '@algorandfoundation/algokit-utils/types/app-spec'

// Edit this to add in your contracts
export const contracts = ['HelloWorldApp'] as const

export async function deploy(name: (typeof contracts)[number], appSpec: AppSpec) {
  const algod = algokit.getAlgoClient()
  const indexer = algokit.getAlgoIndexerClient()
  const deployer = await algokit.getAccount({ name: 'DEPLOYER', fundWith: algokit.algos(3) }, algod)
  await algokit.ensureFunded(
    {
      accountToFund: deployer,
      minSpendingBalance: algokit.algos(2),
      minFundingIncrement: algokit.algos(2),
    },
    algod,
  )
  const isLocal = await algokit.isLocalNet(algod)
  const appClient = algokit.getAppClient(
    {
      app: appSpec,
      sender: deployer,
      creatorAddress: deployer.addr,
      indexer,
    },
    algod,
  )

  switch (name) {
    // Edit this to add the custom deployment logic for each contract
    case 'HelloWorldApp':
      const app = await appClient.deploy({
        allowDelete: isLocal,
        allowUpdate: isLocal,
        onSchemaBreak: isLocal ? 'replace' : 'fail',
        onUpdate: isLocal ? 'update' : 'fail',
      })
      // If app was just created fund the app account
      if (['create', 'replace'].includes(app.operationPerformed)) {
        algokit.transferAlgos(
          {
            amount: algokit.algos(1),
            from: deployer,
            to: app.appAddress,
          },
          algod,
        )
      }

      const method = 'hello'
      const methodArgs = ['world']
      const response = await appClient.call({ method: method, methodArgs: methodArgs })
      console.log(
        `Called ${method} on ${name} (${app.appId}) with args=[${methodArgs}], received: ${response.return?.returnValue}`,
      )
      break
    default:
      throw new Error(`Attempt to deploy unknown contract ${name}`)
  }
}
