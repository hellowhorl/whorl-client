# Setting up Whorl-Client

## Prerequisites 
1. Clone the client repository 

    ```sh
    git clone git@github.com:allegheny-college-cmpsc-404-spring-2025/whorl-client.git
    ``` 

2. Setup a virtual environment 

    here you work to utilize `venv` short for virtual environment specific for your client. 

    ```sh
    python -m venv .venv
    ``` 
    then run this next command 
    Source .venv/bin/activate
    ```
    PSA - your virtual environment will stay open so when finish run comand 'deactivate'

3. once your virtual environment is finished being set up perform a development install python -m pip install -e 

4. The client repository requires .env files using dotenv.org to manage our files you will need to have nodejs instaalled to your machine and you will download it using the npx command 

    https://nodejs.org/en/download 

5. lastly you will need to access the client through your machine and access the main folder then you will run npx dotenv-vault@latest pull

# Testing whorl-client locally

## Prerequisites

1. Clone the Repository:

    ```sh
    git clone https://github.com/whorlassignments/starship-assignment.git
    ```

2. Set Up Your Environment:

    Utilize the `venv` of your whorl-client project to run the following commands (use the repository of `whorl-client` and cd to `starship-assignment`).

## Collect Required Items

You will need to move between directories ("rooms") to collect specific Python files, which will act as "items" in your inventory.

Move from "room" to "room" and use the `get` command to add the necessary Python files to your inventory. Here's what you need to collect:

- 3 Copies of `Sprocket.py`
- 1 Copy of `FluxCapacitor.py`
- 1 Copy of `ThermoCube.py`

To collect these items, navigate to the respective folder and type:

```sh
get FILENAME.py
```

Use the `inventory` command to check your collected items.

## Start the Engine

Once you have all the required files in your inventory, navigate to the `engine-room` directory and run the engine:

```sh
./Engine
```

## Verify the Engine Status

If the engine starts successfully, proceed to the `bridge` directory and run:

```sh
./Controls
```

This should confirm that the engine has started.

## Example Walkthrough

- **Navigate to Rooms:** Use `cd` to move between directories and collect the required files.
- **Check Inventory:** Periodically verify your inventory to ensure you have all the necessary items.
- **Start and Verify:** Follow the steps above to start the engine and confirm it through the controls.

## Notes

- Each file must be explicitly collected by typing `get FILENAME.py` in the appropriate directory.
- The sequence of operations matters: ensure you have all items before starting the engine.

By following these steps, you can confirm that the whorl-client functions as intended!
