import {
  AlgoAmount,
  getAccount,
  getAlgoClient,
  getAlgoIndexerClient,
  isLocalNet,
  transferAlgos,
  ApplicationClient,
} from '@algorandfoundation/algokit-utils'
import { AppSpec } from '@algorandfoundation/algokit-utils/types/appspec'

// Edit this to add in your contracts
export const contracts = ['HelloWorldApp'] as const

export async function deploy(name: (typeof contracts)[number], appSpec: AppSpec) {
  const algod = getAlgoClient()
  const indexer = getAlgoIndexerClient()
  const deployer = await getAccount({ name: 'DEPLOYER', fundWith: AlgoAmount.Algos(10) }, algod)
  const isLocal = await isLocalNet(algod)
  const appClient = new ApplicationClient(
    {
      app: appSpec,
      sender: deployer,
      creatorAddress: deployer.addr,
    },
    algod,
    indexer,
  )

  switch (name) {
    // Edit this to add the custom deployment logic for each contract
    case 'HelloWorldApp':
      const app = await appClient.deploy({
        version: '1.0',
        allowDelete: isLocal,
        allowUpdate: isLocal,
        onSchemaBreak: isLocal ? 'replace' : 'fail',
        onUpdate: isLocal ? 'update' : 'replace',
      })
      // If app was just created fund the app account
      if (app.operationPerformed === 'create') {
        transferAlgos(
          {
            amount: AlgoAmount.Algos(1),
            from: deployer,
            to: app.appAddress,
          },
          algod,
        )
      }
      break
    default:
      throw new Error(`Attempt to deploy unknown contract ${name}`)
  }
}
