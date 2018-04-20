package com.recommendation.controller;
import com.recommendation.service.TCPService;
import org.json.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import java.util.HashMap;
import java.util.Map;

@Controller
public class SubmitingController {
    @Qualifier("TCPServiceImpl")
    @Autowired
    private TCPService tcpService;
    @RequestMapping("/submit")
    public String doSubmitAction(Model model,
                                @RequestParam("brand") String brand,
                                @RequestParam("campaign_id") String campaign_id,
                                @RequestParam("customer")String customer,
                                @RequestParam("price") String price){
        Map<String,String> map = new HashMap<>();
        map.put("brand", brand);
        map.put("campaign_id", campaign_id);
        map.put("customer", customer);
        map.put("price", price);
        JSONObject jsonpObject = new JSONObject(map);
        JSONObject response = tcpService.doRequest("localhost", 9999, jsonpObject);
        model.addAttribute("result",(String)response.get("response"));
        return "second";
    }
    @RequestMapping("/result")
    public ModelAndView redirect(@RequestParam("name") String name){
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("second");
        modelAndView.addObject("result", name);
        return modelAndView;
    }
    @RequestMapping("/f")
    public String redirect1(){
        return "front";
    }
}
