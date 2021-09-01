def get_financial_cost(similar_product_df):
    financial_cost = similar_product_df["custo_financeiro"].iloc[0]
    if financial_cost == "TJLP":
        financial_cost = "TLP"
    return financial_cost

def encode_test_data(features_lst, training_encoder_dict, training_columns):
    test_data = []
    for feature, column in zip(features_lst, training_columns):
        encoded_feature_value = training_encoder_dict.get(column, {}).get(feature, None)
        if encoded_feature_value is None:
            test_data.append(feature)
        else:
            test_data.append(encoded_feature_value)
    return test_data

def create_decoder_dict(encoder_dict):
    return {v: k for k, v in encoder_dict.items()}

def get_prediction(model, feature_data, encoder_dict, training_columns, label_column):
    encoded_test = encode_test_data(feature_data, encoder_dict, training_columns)
    encoded_prediction = model.predict([encoded_test])[0]
    prediction_prob = max(model.predict_proba([encoded_test])[0])
    decoder_dict = create_decoder_dict(encoder_dict[label_column])
    prediction = decoder_dict[encoded_prediction]
    return prediction, prediction_prob

def get_similar_recent_financing(full_df, filter_column, filter_value, amount_of_money):
    similar_values_df = full_df[full_df[filter_column] == filter_value]
    similar_values_df = similar_values_df.iloc[
        (similar_values_df["valor_contratado_reais"]- amount_of_money).abs().argsort()[:15]
    ]
    similar_values_df.sort_values(by="ano_contratado", inplace=True, ascending=False)
    return similar_values_df[:2].reset_index()

def get_similar_financing(full_df, filter_column, filter_value, company_nature, size_of_company, amount_of_money, innovation, company_sector, company_subsector):
    similar_values_df = full_df[full_df[filter_column] == filter_value]
    similar_values_df = similar_values_df.iloc[(similar_values_df["valor_contratado_reais"]- amount_of_money).abs().argsort()[:15]]
    similar_values_df.sort_values(by="ano_contratado", inplace=True, ascending=False)
    similar_values_df.sort_values(by=["inovacao"], key=lambda x: x.map({innovation: 0}), inplace=True)
    similar_values_df.sort_values(by="natureza_do_cliente", key=lambda x: x.map({company_nature: 0}), inplace=True)
    similar_values_df.sort_values(by=["setor_cnae"], key=lambda x: x.map({company_sector: 0}), inplace=True)
    similar_values_df.sort_values(by=["subsetor_cnae"], key=lambda x: x.map({company_subsector: 0}), inplace=True)
    similar_values_df.sort_values(by=["porte_do_cliente"], key=lambda x: x.map({size_of_company: 0}), inplace=True)
    return similar_values_df[:5].reset_index()

def calculate_time_score(similar_df, today_year):
    time_score = 1/max(today_year - similar_df["ano_contratado"].iloc[0], 1)
    return time_score

def get_weighted_information(full_df, similar_df, financial_cost, amount_of_money, today_year):
    time_score = calculate_time_score(similar_df, today_year)
    wighted_fee = similar_df["juros"].iloc[0] * time_score
    wighted_grace = similar_df["prazo_carencia_meses"].iloc[0] * time_score
    wighted_amortization = similar_df["prazo_amortizacao_meses"].iloc[0] * time_score
    time_score_diff = 1 - time_score

    if time_score_diff > 0:
        similar_recent_df = get_similar_recent_financing(full_df, "custo_financeiro", financial_cost, amount_of_money)
        recent_fee = similar_recent_df["juros"].mean()
        recent_grace_period = similar_recent_df["prazo_carencia_meses"].mean()
        recent_amortization_period = similar_recent_df["prazo_amortizacao_meses"].mean()
        wighted_fee += (time_score_diff * recent_fee)
        wighted_grace +=  (time_score_diff * recent_grace_period)
        wighted_amortization += (time_score_diff * recent_amortization_period)

    return wighted_fee, wighted_grace, wighted_amortization