
import helper_fn as hf
import instructions as ins

# getting the data
data = hf.get_data()

# cleaning the data

# creating a copy of the data
data_1 = data.copy()



response = data_1['model_response'] = data_1['review_full'].apply(
                                                 lambda x: hf.generate_llama_response(ins.instruction_1, x))


print(response)


