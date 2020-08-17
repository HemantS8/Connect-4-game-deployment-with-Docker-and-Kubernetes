import numpy as np
import io
import csv
from flask import Flask, request, render_template
import pickle
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('test.log')
format= "%(asctime)s : %(levelname)s : %(name)s : Line No %(lineno)d : %(message)s"
formatter = logging.Formatter(format)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.info("Prediction Started Successfully")

app = Flask(__name__)
model = pickle.load(open('gradientmodel.pkl', 'rb'))

@app.route('/', methods= ['GET', 'POST'])
def home():
    return render_template('Connect4latesthtml.html')


    
@app.route('/predict', methods= ['GET', 'POST'])
def predict_value_input():
    
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('test.log')
    format= "%(asctime)s : %(levelname)s : %(name)s : Line No %(lineno)d : %(message)s"
    formatter = logging.Formatter(format)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.info("predict_value_input function started successfully")
        
    listb = []
    listp = []
    
    try :
        

        if request.method == 'POST':
            listb.append(request.form['board1'])
            listb.append(request.form['board2'])
            listb.append(request.form['board3'])
            listb.append(request.form['board4'])
            listb.append(request.form['board5'])
            listb.append(request.form['board6'])
            listb.append(request.form['board7'])
            listb.append(request.form['board8'])
        
            listp.append(request.form['pboard1'])
            listp.append(request.form['pboard2'])
            listp.append(request.form['pboard3'])
            listp.append(request.form['pboard4'])
            listp.append(request.form['pboard5'])
            listp.append(request.form['pboard6'])
            listp.append(request.form['pboard7'])
            listp.append(request.form['pboard8'])
        
        

    
        standard = ['atr1','atr2','atr3','atr4','atr5','atr6','atr7','atr8','atr9','atr10','atr11','atr12','atr13','atr14','atr15','atr16','atr17','atr18','atr19','atr20','atr21','atr22','atr23','atr24','atr25','atr26','atr27','atr28','atr29','atr30','atr31','atr32','atr33','atr34','atr35','atr36','atr37','atr38','atr39','atr40','atr41','atr42']    
        standardmodified = []
        standardmodified.extend(standard)
        for i in range(8):
            for j in range(42):
                if (standardmodified[j] == listb[i]):
                    standardmodified[j] = listp[i]
                
                
        for i in range(42):
            if standardmodified[i] == standard[i]:
                standardmodified[i] = 0
        
        
     
    except ValueError :
        raise ValueError
        logger.error('Error occured while taking data from user')
        
    except Exception as e :
        raise e
        logger.error('Exception occured')
        
     
    try:
        
        
        
        '''
        For rendering results on HTML GUI
         '''
        final_features = [np.array(standardmodified)]
        prediction = model.predict(final_features)
    
        if (prediction == 0):
            return render_template('Connect4latesthtml.html', prediction_text='Match will be a {}'.format('Draw'))
        elif (prediction == 1):
            return render_template('Connect4latesthtml.html', prediction_text='First player will be going to {}'.format('Lose'))
        elif (prediction == 2):
            return render_template('Connect4latesthtml.html', prediction_text='First player will be going to {}'.format('Win'))
        
        
        
        
    except Exception as e:
        raise e

        

logger.info('Model worked successfully')


@app.route('/inputfile',methods = ['POST'])
def predict_file_input():
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('test.log')
    format= "%(asctime)s : %(levelname)s : %(name)s : Line No %(lineno)d : %(message)s"
    formatter = logging.Formatter(format)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("predict_file_input function started successfully")
    
    
    try :
        

        if request.method == 'POST':
            f = request.files['addfile']
            stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.reader(stream)
            list_row = list(csv_input)
        
        result =[]
        for i in range(0, len(list_row)):
            for j in range(42):
                test_list = [int(j) for j in list_row[i]]
            file_predict = [np.array(test_list)]
            filepredictfinal= model.predict(file_predict)
            result.append(filepredictfinal)
                
        for k in range(0, len(result)):
            if (result[k] == 2):
                result[k] = 'Win'
            elif (result[k] == 1):
                result[k] = 'Lose'
            elif (result[k] == 0):
                result[k] = 'draw'
        
        return render_template('Connect4latesthtml.html', prediction_text= result)
    
        
    except Exception as e :
        
        raise e
    
    
    
logger.info("Model worked successfully")   
logger.info("Prediction Ended Successfully")
   

if __name__ == "__main__" :
    app.run(debug=True)