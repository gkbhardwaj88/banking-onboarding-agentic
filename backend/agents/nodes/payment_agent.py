def payment_agent(state, method="UPI", amount=100):
    state.payment = {"status":"success","method":method,"amount":amount}
    return state
