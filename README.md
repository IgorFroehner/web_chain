# Web Chain

A flask app for blockchain visualization that saves the text data from users in a **PoW** based "blockchain". 
It had been created for learning purposes and designed to be an open data saving structure as a blockchain is, 
all you need to pay is the computation power of mining your block.

### Requirements

* postgresql
* python3

## Executing

1. `pip3 install -r requirements.txt`
2. Use `create.sql` to create the database
3. Set the config env variable `SQLALCHEMY_DATABASE_URI`
4. Run the app using command `flask run`

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

### postgres DB?

It is a centralized blockchain, and it stores the data into a postgres table. I know it is not the to do that,
and I am open to suggestions and help on this point.

