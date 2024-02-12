import csv
import json
import os

from components.commands import logger, deviceInfo, getIndex, cameraID
from components.camera import Camera
import components.constants as constants
from components.gif import exportGif

class ApiWeb:
    def __init__(self, database):
        def handle_message(client, userdata, message):
            try:
                data = json.loads(message.payload.decode())
                if message.topic == "status":

                elif message.topic == "comandos":
                    if (data.get("interface") == "exportGif"):
                        exportGif('above', self.filePrefix, self.data_path)
                    elif (data.get("interface") == "send_data"):
                        self.camera1.save_frame(getIndex(self.last_position), self.filePrefix, self.data_path, self.last_position)
                else:
                    topic = message.topic.split('/')[1]
                    self.database.run_query(self.database.querys[topic], tuple(data.values()))
                    self.sensores[topic] = data
                    self.csv_writter(topic, data)
            except Exception as e:
                print (e)

        self.filePrefix = database.run_query("SELECT * FROM db.config WHERE name='prefix'")[0][2]
        self.sensores = {}
        self.data_path = '/csvFiles'
        self.camera1 = Camera(cameraID()['above'], "above")
        self.camera2 = Camera(cameraID()['below'], "below")
        self.camera1 = Camera(0, "above")
        self.last_position = {'x' : 0, 'y' : 0, 'z' : 0}
        self.routes()

    def __call__(self):
        return self.page

    

    def csv_writter(self, sensor: str = 'nosensor', sensorData: dict = {}):
        os.makedirs(f'{self.data_path}/{self.filePrefix}/csv/', exist_ok=True)
        file_name = f'{self.data_path}/{self.filePrefix}/csv/{sensor}.csv'
        sensorData['id'] = getIndex(self.last_position)
        sensorData['x_pos'] = self.last_position['x']
        sensorData['y_pos'] = self.last_position['y']
        sensorData['z_pos'] = self.last_position['z']
        if os.path.exists(file_name):
            with open(file_name, mode='a') as file:
                writter = csv.writer(
                    file)
                writter.writerow(list(sensorData.values()))
                file.close()
        else:
            with open(file_name, mode='x') as file:
                writter = csv.DictWriter(
                    file, fieldnames=list(sensorData.keys()))
                writter.writeheader()
                writter.writerow(sensorData)
                file.close()

    def routes(self):
        @self.page.route('/')
        def home():
            return render_template('index.html', prefix=self.filePrefix)

        @self.page.route('/data/<sensor>', methods = ['POST'])
        def data(sensor):
            returnD = (self.database.select_datetime(sensor, request.json.get('dateInit', constants.dateInit), request.json.get('dateEnd', constants.dateEnd))) # type: ignore
            return returnD

        @self.page.route('/sensors')
        def sensores():
            return (self.sensores)

        @self.page.route('/changePrefix/<id>')
        def change_prefix(id):
            self.filePrefix = id
            self.database.run_query(f"UPDATE db.config SET data='{id}' WHERE name='prefix'")
            return redirect('/')
        
        @self.page.route('/download')
        def download():
            return render_template('downloadData.html', files=os.listdir(self.data_path))

        
        def downloadFile(file):
            os.system(f'zip -r {self.data_path}/{file}.zip {self.data_path}/{file}')
            @after_this_request
            def remove_file(response):
                print ('2')
                try:
                    os.remove(f'{self.data_path}/{file}.zip')
                    pass
                except Exception as error:
                    pass
                return redirect('/download')
            print ('1')
            return send_from_directory(self.data_path, f'{file}.zip', as_attachment=True)
        
        @self.page.route('/downloadFile/<file>')
        def downloadFile2(file):
            exportGif('above', self.filePrefix, self.data_path)
            cwd = os.getcwd()
            os.system(f'cd {self.data_path} && zip -r {file}.zip {file} && cd {cwd}')
            with open(os.path.join(self.data_path, f'{file}.zip'), 'rb') as f:
                data = f.readlines()
            os.remove(os.path.join(self.data_path, f'{file}.zip'))
            return Response(data, headers={'Content-Type': 'application/zip','Content-Disposition': 'attachment; filename=%s;' % f'{file}.zip'})
        
        @self.page.route('/deviceInfo')
        def api_device():
            deviceInfo()
            return deviceInfo()
        
        @self.page.route('/cameras')
        def cameras():
            return render_template('cameras.html')

        @self.page.route("/screenshot", methods =['POST'])
        def screenshot():
            cameras = {'above':self.camera1, 'below':self.camera2, None : None}
            return Response(self.gen_screenshot(cameras[request.json.get('camera')]),mimetype='image/jpeg') # type: ignore
