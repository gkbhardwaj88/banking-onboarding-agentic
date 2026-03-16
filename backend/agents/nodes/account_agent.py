def account_agent(state, account_type="SAVINGS"):
    state.account = {
        "account_type": account_type,
        "account_number": "ACC"+str(state.user_id or 1000)
    }
    return state
