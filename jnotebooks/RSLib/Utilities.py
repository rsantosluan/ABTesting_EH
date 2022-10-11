import numpy  as np  
import pickle as pkl

### 
from statsmodels.stats import api as sms


class ab_testing():

    def calculo_tamanho_amostra( data_raw, pais,indicador = 0, lift = 0.05, alpha = 0.05, power = 0.80 ):
        '''
        Deverão ser passados:
        - Dataframe 
        - pais  (BRA, USA...)
        - indicador (spent se = 0 | purcheases se = 1)
        - lift  (Por padrão 0.05)
        - alpha (Por padrão 0.05)
        - power (Por padrão 0.80)
        '''
        ## Dataframe auxiliar contendo média e desvio padrão dos dados referentes ao Brasil        
        if indicador == 0:
            df_aux = data_raw.loc[data_raw.country == pais].spent.agg( ['mean', 'std'] )
        elif indicador == 1:
            df_aux = data_raw.loc[data_raw.country == pais].purchases.agg( ['mean', 'std'] )    
        else:
            return print( 'Opção incorreta' )    

        ## A métrica inicial receberá a média dos gastos referente a toda a amostra
        metric_ini = df_aux['mean']
        ## A métrica final receberá a média dos gastos mais a margem (lift) de 5%
        metric_fin = metric_ini * (1 + lift)
        ## Desvio padrão referente a toda a amostra de dados
        std_metric = df_aux['std']

        ## Cálculo do tamanho do efeito
        effect_size = ( metric_fin - metric_ini ) / std_metric

        ## Cálculo do tamanho mínimo de amostra
        sample_size = sms.tt_ind_solve_power(
            effect_size = effect_size,
            alpha = alpha,
            power = power
        )
        real_size = len( data_raw.loc[data_raw.country == pais] )
        return np.ceil( sample_size ).astype( int ), real_size       

class plot_grafico():
    def plot_values_vbar( ax ):
        for i in ax.patches:
            if i == 0:
                None
            else:
                ax.annotate(
                #Texto a ser plotado
                round(i.get_height()),
                #Posição horizontal
                (i.get_x() + i.get_width() /2, i.get_height() + i.get_height() /80 ),
                ha='center' ,   
                color='black',
                fontsize=15
    );  
        return None        