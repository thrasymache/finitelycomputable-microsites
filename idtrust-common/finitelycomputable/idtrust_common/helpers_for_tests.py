from finitelycomputable.idtrust_common.strategies import Strategy

reveal_trust_data = {
    'user_intent': 'Trust',
    'user_miscommunication': 0.1,
    'foil_miscommunication': 0.1,
}
reveal_distrust_data = {
    'user_intent': 'Distrust',
    'user_miscommunication': 0.1,
    'foil_miscommunication': 0.1,
}
user_guess_data = {'user_guess': Strategy.Innocent.value}
distrust_data = {'user_intent': 'Distrust'}
trust_data = {'user_intent': 'Trust'}

home_blind_url = '/'
# response = client.post('/identification_of_trust/',
home_reveal_url = '/choose_miscommunication'
# response = client.get('/identification_of_trust/choose_miscommunication')
journey_blind_url = '/journey/1'
#response = client.post('/identification_of_trust/journey/1',
journey_2_blind_url = '/journey/2'
#response = client.post('/identification_of_trust/journey/2',
journey_reveal_url = '/journey/1/choose_miscommunication'
#'/identification_of_trust/journey/1/choose_miscommunication', {
journey_2_reveal_url = '/journey/2/choose_miscommunication'
#'/identification_of_trust/journey/2/choose_miscommunication', {
interaction_url = '/interact/1'
#'/identification_of_trust/interact/1'

