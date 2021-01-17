from PyQt5.QtCore import QObject, pyqtSignal
import pandas as pd
from packages.model import common_model


class Overall(QObject):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.data = self.load_data()
        self.agent_fee = self.summarize_agent_fee()

    def load_data(self):
        df = pd.read_excel(self.file_path, sheet_name='Overall', skiprows=3)
        df.columns = self.modify_column_names(df)
        id_player_dict = self.get_id_player_dict(df)

        # drop unnecessary data
        df = df.iloc[1:, 1:]
        df = df.loc[df['player_id'].notna()]

        # add player_winnings + agent name
        df['player_winnings:overall'] =\
            df.loc[:, 'player_winnings:from_opponents':'player_winnings:from_jackpot'].sum(axis=1)
        df['agent_name'] = df['player_id'].map(id_player_dict)
        return df

    @staticmethod
    def get_columns(df):
        main_columns = pd.Series(df.columns)
        sub_columns = df.iloc[0]
        return main_columns, sub_columns

    def modify_column_names(self, df):
        main_columns, sub_columns = self.get_columns(df)
        modified_columns = common_model.modify_column_names(main_columns, sub_columns)
        return modified_columns

    @staticmethod
    def get_id_player_dict(modified_df):
        id_player_series = modified_df[['player_id', 'nickname']].set_index('player_id')
        id_player_series.drop_duplicates(inplace=True)
        id_player_dict = id_player_series.to_dict('dict')['nickname']
        return id_player_dict

    def summarize_agent_fee(self):
        agent_fee = self.data.groupby(['agent_id', 'agent', 'agent_name'])[['club_earnings:fee']].sum()
        agent_fee.sort_values(by='club_earnings:fee', ascending=False, inplace=True)
        agent_fee.reset_index(inplace=True)
        return agent_fee


if __name__ == '__main__':
    overall = Overall(r'C:\Users\KelvinG\Documents\GitHub\ClubDataSummarizer\dummy_data.xlsx')
    overall.generate_overall_summary()
    print(overall.data)
    print(overall.agent_fee)

