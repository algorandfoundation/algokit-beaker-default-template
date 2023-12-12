import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { HelloWorldClient } from '../smart_contracts/artifacts/hello_world/client'
import { Account, Algodv2, Indexer } from 'algosdk'

describe('hello world contract', () => {
  const localnet = algorandFixture()
  beforeEach(localnet.beforeEach)

  const deploy = async (account: Account, algod: Algodv2, indexer: Indexer) => {
    const client = new HelloWorldClient(
      {
        resolveBy: 'creatorAndName',
        findExistingUsing: indexer,
        sender: account,
        creatorAddress: account.addr,
      },
      algod,
    )
    await client.deploy({
      allowDelete: true,
      allowUpdate: true,
      onSchemaBreak: 'replace',
      onUpdate: 'update',
    })
    return { client }
  }

  test('says hello', async () => {
    const { algod, indexer, testAccount } = localnet.context
    const { client } = await deploy(testAccount, algod, indexer)

    const result = await client.hello({ name: 'World' })

    expect(result.return).toBe('Hello, World')
  })

  test('simulate says hello with correct budget consumed', async () => {
    const { algod, indexer, testAccount } = localnet.context
    const { client } = await deploy(testAccount, algod, indexer)
    const atc = await client.compose().hello({ name: 'World' }).hello({ name: 'Jane' }).atc()

    const result = await atc.simulate(algod)

    expect(result.methodResults[0].returnValue).toBe('Hello, World')
    expect(result.methodResults[1].returnValue).toBe('Hello, Jane')
    expect(result.simulateResponse.txnGroups[0].appBudgetConsumed).toBe(98)
  })
})
