from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')
row = soup.find_all('tr', attrs={'class':''})
row_length = len(row)

temp = [] #init

for i in range(0, row_length):
    
    # get tanggal
    tanggal = row[i].find_all('td', attrs={'class' : ''})[0].text
    
    # get harga_harian
    harga_harian = row[i].find_all('a', attrs={'class' : ''})[0].text
    harga_harian = harga_harian.strip() #to remove excess white space
    
    
    temp.append((tanggal,harga_harian)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('tanggal','harga_harian'))

#insert data wrangling here
df['harga_harian'] = df['harga_harian'].str.replace(",","")
df['harga_harian'] = df['harga_harian'].astype('float64')
df['tanggal'] = df['tanggal'].astype('datetime64')

df = df.set_index('tanggal')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["harga_harian"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)