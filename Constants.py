def prompt_for_email(email, jsonFormatted) :
	pre_input = ('You are an international trip planner who organizes and coordinates all aspects of a flight, '
		'including route planning, obtaining permits, fuel calculations, weather analysis, and airport arrangements.'
		'They monitor the flight in real-time, handle any in-flight issues, and ensure compliance with regulations. '
		'Post-flight, they manage customs, billing, and maintenance, ensuring a smooth and efficient journey for both passengers and crew.'
		' Based the following email (')
	json_format = ". Please provide the output as a JSON-formatted string only. Do not include any explanations, text, or comments—just the JSON." if jsonFormatted == True else ""
	post_input = (') received from customer for the new trip planning, you are supposed to extract and format the data in below structure.' 
				 'The format is as follows:'
				 'Trip Details:'
			     'Leg 1 - Sector 1'
			     'Departure Airport'
			     'Arrival Airport'
			     'Departure Time'
			     'Arrival Time'
			     'PAX (Passenger Details)'
			     'Crew (Pilot & Cabin Crew Details)'
			     'Services Requested( Can be Ground Handling, Fuel, Hotel Arrangement etc.). Provide only the trip details and do not include any additional text or comments at the start and end of your response.')
	gpt_prompt = "".join([pre_input, email, post_input, json_format])
	# print(gpt_prompt)
	return gpt_prompt