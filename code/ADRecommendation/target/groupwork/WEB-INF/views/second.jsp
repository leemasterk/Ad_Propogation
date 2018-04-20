<!DOCTYPE html>
<%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Ad Recommend</title>
    <link rel="stylesheet" href="<%=request.getContextPath()%>/resources/css/second.css">
</head>
<body>
<div id="container_body">
    <div algin= "center" id="body">
        <div class="row">
            <div class="row-content">
                <p class="header">Recommend Result</p>
                <p><textarea class="input">${result}</textarea></p>
            </div>
        </div>
        <div class="logoBox"><img src="<%=request.getContextPath()%>/resources/img/recommend.png" alt="" class="logo"></div>
    </div>
</div>
</body>
</html>