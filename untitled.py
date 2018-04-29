from web3 import Web3, HTTPProvider, TestRPCProvider, WebsocketProvider
from solc import compile_source
from web3.contract import ConciseContract
from eth_utils import to_checksum_address

contract_source_code = '''
pragma solidity ^0.4.11;

/// @title Listing
/// @dev Used to keep marketplace of listings for buyers and sellers
/// @author Matt Liu <matt@originprotocol.com>, Josh Fraser <josh@originprotocol.com>, Stan James <stan@originprotocol.com>

import "./Listing.sol";

contract ListingsRegistry {

  /*
   * Events
   */

  event NewListing(uint _index);

  /*
   * Storage
   */

  // Contract owner
  address public owner;

  // Array of all listings
  Listing[] public listings;


  /*
   * Modifiers
   */
  modifier isValidListingIndex(uint _index) {
    require (_index < listings.length);
    _;
  }


  modifier isOwner() {
    require (msg.sender == owner);
    _;
  }


  /*
   * Public functions
   */

  function ListingsRegistry()
    public
  {
    // Defines origin admin address - may be removed for public deployment
    owner = msg.sender;

    // Sample Listings - May be removed for public deployment
    // 2018-04-04 - Temp commented out to get under gas limit.
    // testingAddSampleListings();
  }

  function testingAddSampleListings()
    public
    isOwner
  {
    // We get stripped hex value from IPFS hash using getBytes32FromIpfsHash()
    // in contract-service.js

    // Zinc house - Hash: QmTfozaMrUBZdYBzPgxuSC15zBRgLCEfQmWFZwmDHYGY1e
    create(
      0x4f32f7a7d40b4d65a917926cbfd8fd521483e7472bcc4d024179735622447dc9,
      3.999 ether, 1
    );

    // Scout II - Hash: QmZD8wZWEqzKwvEtGWXzCb3MuXvmxLdCxXGHMRocQFnpoy
    create(
      0xa183d4eb3552e730c2dd3df91384426eb88879869b890ad12698320d8b88cb48,
      0.600 ether, 1
    );

    // Mamalahoa Estate - Hash: QmZtQDL4UjQWryQLjsS5JUsbdbn2B27Tmvz2gvLkw7wmmb
    create(
      0xab92c0500ba26fa6f5244f8ba54746e15dd455a7c99a67f0e8f8868c8fab4a1a,
      8.500 ether, 1
    );

    // Casa Wolf - Hash: QmVYeipL2JWFkpWsGqNNXDFUVAmPWEEK8u3Q45CZ1YrZPf
    create(
      0x6b14cac30356789cd0c39fec0acc2176c3573abdb799f3b17ccc6972ab4d39ba,
      1.500 ether, 1
    );

    // Taylor Swift - Hash: QmfXRgtSbrGggApvaFCa88ofeNQP79G18DpWaSW1Wya1u8
    create(
      0xff5957ff4035d28dcee79e65aa4124a4de4dcc8cb028faca54c883a5497d8917,
      0.300 ether, 25
    );

    // // Red shoe - Hash: QmfF4JBA4fEYDkZqjRHnDxWGGoXg5D1T4WqfDrN4GXP33p
    // create(
    //   0xfb27dcfe2c7febe98d755e2f9df0ff73fb8abecaa778f540d0cbf28b059306db,
    //   0.01 ether, 1
    // );

    // // Lambo - Hash: QmYsNo3fYTXQRHREYeoGUGLuYETnjx3HxQFMeiZuE7zPSf
    // create(
    //   0x9c73e11ffa575504295be4ece1d4ea49df33261f8eb6a4a7e313e4bb74abf150,
    //   2.50 ether, 1
    // );
  }

  /// @dev listingsLength(): Return number of listings
  function listingsLength()
    public
    constant
    returns (uint)
  {
      return listings.length;
  }

  /// @dev getListing(): Return listing info for given listing
  /// @param _index the index of the listing we want info about
  function getListing(uint _index)
    public
    constant
    returns (Listing, address, bytes32, uint, uint)
  {
    // Test in truffle deelop:
    // ListingsRegistry.deployed().then(function(instance){ return instance.getListing.call(0) })

    // TODO (Stan): Determine if less gas to do one array lookup into var, and
    // return var struct parts
    return (
      listings[_index],
      listings[_index].owner(),
      listings[_index].ipfsHash(),
      listings[_index].price(),
      listings[_index].unitsAvailable()
    );
  }

  /// @dev create(): Create a new listing
  /// @param _ipfsHash Hash of data on ipfsHash
  /// @param _price Price of unit. Currently ETH, will change to 0T
  /// @param _unitsAvailable Number of units availabe for sale at start
  ///
  /// Sample Remix invocation:
  /// ["0x01","0x7d","0xfd","0x85","0xd4","0xf6","0xcb","0x4d","0xcd","0x71","0x5a","0x88","0x10","0x1f","0x7b","0x1f","0x06","0xcd","0x1e","0x00","0x9b","0x23","0x27","0xa0","0x80","0x9d","0x01","0xeb","0x9c","0x91","0xf2","0x31"],"3140000000000000000",42
  function create(
    bytes32 _ipfsHash,
    uint _price,
    uint _unitsAvailable
  )
    public
    returns (uint)
  {
    listings.push(new Listing(msg.sender, _ipfsHash, _price, _unitsAvailable));
    NewListing(listings.length-1);
    return listings.length;
  }


}
'''

# compiled_sol = compile_source(contract_source_code)
# # Compiled source code
# contract_interface = compiled_sol['<stdin>:Listing']

# w3 = Web3(WebsocketProvider('wss://rinkeby.infura.io/_ws'))

# contract_instance = w3.eth.contract(address='0x94dE52186b535cB06cA31dEb1fBd4541A824aC6d',abi=contract_interface['abi'])


# print(w3.eth.blockNumber)
# print(contract_instance.eventFilter('ListingPurchased', {'fromBlock':0,'toBlock':'latest'}).get_all_entries())
import json

def get_contract_abi(contract_name):
    with open("./contracts/{}.json".format(contract_name)) as f:
        print(contract_name)
        contract_interface = json.loads(f.read())
        return contract_interface['abi']


class ContractParser(object):

    def __init__(self, event_type, contract_address, block_from=0, block_to='latest'):
        self.event_type = event_type
        self.block_from = block_from
        self.block_to = block_to
        self.contract_address = contract_address
        self.abi = get_contract_abi('Purchase')

    @property
    def block_reference_dict(self):
        return {"fromBlock": self.block_from,
                "toBlock": self.block_to}

    # def get_web3(self):
    #     return Web3(WebsocketProvider('wss://rinkeby.infura.io/_ws'))

    def get_web3(self):
        return Web3(HTTPProvider('http://127.0.0.1:9545'))

    def get_contract(self):
        contract = self.get_web3().eth.contract(address=self.contract_address,
                                                abi=self.abi)
        return contract

    # def get_events(self, fetch_new=False):
    #     event = self.get_contract().events.ListingPurchased.createFilter(fromBlock=0, toBlock='latest')
    #     import pdb
    #     pdb.set_trace()
    #     return event.get_all_entries()

    def get_events(self, fetch_new=False):
        event = self.get_contract().eventFilter(self.event_type,
                                                self.block_reference_dict)
        return event.get_new_entries() if fetch_new else\
            event.get_all_entries()

    def get_eventy(self, fetch_new=False):
        w3 = self.get_web3()
        event_name_hashes = []
        event_names = ['ListingPurchased(address)']
        for name in event_names:
            event_name_hashes.append(w3.sha3(text=name).hex())
        print(event_name_hashes)
        event = self.get_web3().eth.filter({
            "topics": [event_name_hashes],
            "fromBlock": 0
        })
        return event.get_all_entries()

cusp = ContractParser('Purchase',
                      to_checksum_address('0x9deee0195f88caf7dee2fa8a6777f8236d847ef8'))


# print(cusp.abi)

l = cusp.get_eventy()
print(len(l))

from util.contract import ContractHelper
for i in l:
    payload = i

    contract_helper = ContractHelper()
    purchase_address = contract_helper.convert_event_data('ListingPurchased',
                                                          payload['data'])
    contract = contract_helper.get_instance('Purchase',
                                            purchase_address)
    print(purchase_address, "+++++++++++++++++++++")

    purchase_data = contract.functions.data().call()

# con = c.get_contract().functions.getListing(2).call()

# # print(con)
# print(Web3.sha3(text='NewListing(uint256)'))2