"""def transferdomain(self, data):

        Creates (and submits to local node and network) a tx to transfer balance from DFI/ETH address to DFI/ETH address.


        Arguments:
        1. array                        (json array, required) A json array of src and dst json objects
             [
               {                        (json object)
                 "src": {               (json object) Source arguments
                   "address": "str",    (string, required) Source address
                   "amount": "str",     (string, required) Amount transfered, the value is amount in amount@token format
                   "domain": n,         (numeric, required) Domain of source: 1 - DVM, 2 - EVM
                   "data": "str",       (string) Optional data
                 },
                 "dst": {               (json object) Destination arguments
                   "address": "str",    (string, required) Destination address
                   "amount": "str",     (string, required) Amount transfered, the value is amount in amount@token format
                   "domain": n,         (numeric, required) Domain of source: 1 - DVM, 2 - EVM
                   "data": "str",       (string) Optional data
                 },
               },
               ...
             ]

        Result:
        "hash"                  (string) The hex-encoded hash of broadcasted transaction

        Examples:
        > defi-cli transferdomain '[{"src":{"address":"<DFI_address>", "amount":"1.0@DFI", "domain": 1}, "dst":{"address":"<ETH_address>", "amount":"1.0@DFI", "domain": 2}}]'
        > defi-cli transferdomain '[{"src":{"address":"<ETH_address>", "amount":"1.0@DFI", "domain": 2}, "dst":{"address":"<DFI_address>", "amount":"1.0@DFI", "domain": 1}}]'




        return self._node._rpc.call("transferdomain", data)"""