# Web Chain

A flask app for blockchain visualization that saves the text data from users in a **PoW** based "blockchain". It had been created for purposes.


### Block Structure

* **index**: The integer block index in the blockchain.

* **version**: The number version of the blockchain where the block was mined.

* **prev_hash**: The string hash of the previous block.

* **hash**: The string hash of this block.

* **time**: Time in UTC that the block was created.

* **nonce**: Integer nonce do block, the variable that can be changed to achieve the hash condition.

* **data**: A string with the data saved to the block.

* **difficulty**: A integer as the difficulty for mining that block.


### Blockchain Structure

* **new_data**: Data that was not already saved to the blockchain.
  
* **chain**: List of the blocks
