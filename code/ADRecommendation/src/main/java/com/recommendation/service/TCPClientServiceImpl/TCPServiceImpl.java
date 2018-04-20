package com.recommendation.service.TCPClientServiceImpl;

import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.Socket;

import com.recommendation.service.TCPService;
import org.json.JSONException;
import org.json.JSONObject;

import org.springframework.stereotype.Service;

@Service
public class TCPServiceImpl implements TCPService {
	private Socket socket;
	public void setSocke(String IP, int port){
		try {
			socket = new Socket(IP,port); 
		} catch (Exception e) {
			// TODO: handle exception
		}
	}
	public Socket getSocket() {
		try{
			return socket;
		}catch (NullPointerException e) {
			e.printStackTrace();
			return new Socket();
		}
	}
	public void close() throws IOException{
		if(socket!=null&&socket.isClosed()!= true){
			socket.close();
		}
	}
	@Override
	public JSONObject doRequest(String IP, int port, JSONObject requestJsonObject){
		// init socket
		try {
			setSocke(IP, port);
			// send data 
			PrintWriter pw = new PrintWriter(socket.getOutputStream());
			pw.println(requestJsonObject.toString());
			System.out.println(requestJsonObject.toString());
			pw.flush();
			//debug
			System.out.println("Json data send to another server");
			//get Response
			InputStream input = socket.getInputStream();
            byte[] data = new byte[10240];
            int recved =  input.read(data);
            String result = null;
            if (recved<1024){
                result = new String(data,0,recved);
            }	
			
			JSONObject responseJsonObject = new JSONObject(result);
			System.out.println(responseJsonObject.get("response"));
			close();
			return responseJsonObject;
			
		} catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return new JSONObject();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return new JSONObject();
		} 
	}
}
