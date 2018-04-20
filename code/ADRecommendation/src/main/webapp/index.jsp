<%--
  Created by IntelliJ IDEA.
  User: kaidiwang
  Date: 27/3/18
  Time: 下午7:12
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Ad Recommend</title>
    <link rel="stylesheet" href="<%=request.getContextPath()%>/resources/css/index.css">
</head>
<body>
<div id="container_body">
    <div id="body">
        <div class="row">
            <div class="row-content">
                <p class="header">Find Your Target</p>
                <form action="<%= request.getContextPath()%>/submit" method="post">
                    <p><input class="input" placeholder=" AD Brand" name="brand"/></p>
                    <p><input class="input" placeholder=" AD Position" name="campaign_id"/></p>
                    <p><input class="input" placeholder=" AD Advertiser" name="customer"/></p>
                    <p><input class="input" placeholder=" Retail Price" name="price"/></p>
                    <div class="btnBox">
                        <input type="submit" class="btn" value="Submit"/>
                    </div>
                </form>
            </div>
        </div>
        <div class="logoBox"><img src="<%=request.getContextPath()%>/resources/img/recommend.png" alt="" class="logo"></div>
    </div>
</div>
<script src="<%=request.getContextPath()%>/resources/js/jquery.js"></script>
<script>
</script>
</body>
</html>
