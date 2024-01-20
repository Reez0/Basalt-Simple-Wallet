# Basalt Simple Wallet

A simple wallet created using the Stellar XLM Python SDK. This project utilizes Django Rest Framework to create API endpoints and features a dockerized Postgres Database. Authentication is implemented using statically generated tokens, all encapsulated within an Angular frontend. Message queuing functionality is available via Redis and Celery.

## Getting Started

1. Clone or download the repository.
2. Build the Docker container: `docker-compose -f docker-compose.dev.yml up -d –build`
3. Navigate to the Angular project: `cd basalt-simple-wallet`
4. Install dependencies: `npm install`
5. Start the Angular development server: `ng serve`

## Requirements Met

### 1. Creation of an Account

Users can create an account by providing an email address and password. A new wallet is generated for them on the Stellar XLM test network, and their public and private keys are encrypted and stored in a database. A static authentication token is also generated for the user.

### 2. Account Login

Users can log in by providing their account email address and password. The generated token is stored and used for any endpoints protected by token authentication.

### 3. Transaction History

A brief summary of a user's transaction history is provided by retrieving data from the Stellar XLM test network blockchain.

### 4. Balance of Account

Users can view the basic balance of their account. Upon registration, their account is credited with 10,000 Stellar XLM.

### 5. Credit of Account

An account can be topped up with a Stellar XLM transaction, and the transaction is recorded.

### 6. Debit of Account

An account can perform transactions with other users by providing a valid public key.

Feel free to explore and contribute to the development of the Basalt Simple Wallet!