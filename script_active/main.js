const {app, BrowserWindow,
        ipcMain, globalShortcut} = require('electron')
const path = require('path')
const url = require('url')

module.paths.push('C:/Users/youease_server01/AppData/Roaming/npm/node_modules')


// ����һ������ window �����ȫ�����ã�����㲻��������
// �� JavaScript �����������գ� window �ᱻ�Զ��عر�
let win

function createWindow () {
  // ������������ڡ�
  win = new BrowserWindow({width: 800, 
                            height: 600,
                            frame: false,
                            transparent: true,
                            icon: "./static/favicon.ico",
                            resizable: false,
                            x: 200,
                            y: 500
                            });
  win.setMenu(null);

  // Ȼ�����Ӧ�õ� index.html��
  win.loadURL(url.format({
    pathname: path.join(__dirname, 'main.html'),
    protocol: 'file:',
    slashes: true
  }))

  // �򿪿����߹��ߡ�
 win.webContents.openDevTools()

  // �� window ���رգ�����¼��ᱻ������
  win.on('closed', () => {
    // ȡ������ window ����������Ӧ��֧�ֶര�ڵĻ���
    // ͨ����Ѷ�� window ��������һ���������棬
    // ���ͬʱ����Ӧ��ɾ����Ӧ��Ԫ�ء�
    win = null
  })
}

// Electron ���ڳ�ʼ����׼��
// �������������ʱ���������������
// ���� API �� ready �¼����������ʹ�á�
app.on('ready', () => {
    createWindow();
    globalShortcut.register('Ctrl+F12', () => {
            win.webContents.openDevTools();
    
        });

    globalShortcut.register('F5', () => {
      win.loadURL(url.format({
        pathname: path.join(__dirname, 'main.html'),
        protocol: 'file:',
        slashes: true
      }));

    });
});

// ��ȫ�����ڹر�ʱ�˳���
app.on('window-all-closed', () => {
  // �� macOS �ϣ������û��� Cmd + Q ȷ�����˳���
  // ������󲿷�Ӧ�ü���˵����ᱣ�ּ��
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // ��macOS�ϣ�������dockͼ�겢��û���������ڴ�ʱ��
  // ͨ����Ӧ�ó��������´���һ�����ڡ�
  if (win === null) {
    createWindow()
  }
})

// �����ļ����������дӦ��ʣ�������̴��롣
// Ҳ���Բ�ֳɼ����ļ���Ȼ���� require ���롣



function do_quit(e, arg){app.quit();}

ipcMain.on("quit_app", do_quit);

///

//�������ָ��
//electron-packager . --win --out=activetool --arch=x64 --version=1.0.0 --electron-version=1.7.10 --overwrite --icon=./static/favicon.ico
