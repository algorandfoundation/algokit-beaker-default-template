import * as algokit from '@algorandfoundation/algokit-utils'
import { AppSpec } from '@algorandfoundation/algokit-utils/types/app-spec'
import { HelloWorldAppClient } from './artifacts/hello_world_app/client'

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
  const isMainNet = await algokit.isMainNet(algod)
  const appClient = new HelloWorldAppClient(
    {
      resolveBy: 'creatorAndName',
      findExistingUsing: indexer,
      sender: deployer,
      creatorAddress: deployer.addr,
    },
    algod,
  )

  switch (name) {
    // Edit this to add the custom deployment logic for each contract
    case 'HelloWorldApp':
      const app = await appClient.deploy({
        allowDelete: !isMainNet,
        allowUpdate: !isMainNet,
        onSchemaBreak: isMainNet ? 'append' : 'replace',
        onUpdate: isMainNet ? 'append' : 'update',
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
      const response = await appClient.hello({ name: 'world' })
      console.log(`Called ${method} on ${name} (${app.appId}) with name = world, received: ${response.return}`)
      break
    default:
      throw new Error(`Attempt to deploy unknown contract ${name}`)
  }
}
