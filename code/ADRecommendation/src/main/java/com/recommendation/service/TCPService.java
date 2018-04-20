package com.recommendation.service;

import java.net.Socket;

import org.json.JSONObject;
import org.springframework.stereotype.Service;

@Service
public interface TCPService {
	public JSONObject doRequest(String IP, int port, JSONObject requestJsonObject);
}
