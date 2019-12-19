<%@page import="com.bigdata2019.emaillist.dao.Emaillistdao"%>
<%@page import="com.bigdata2019.emaillist.vo.Emaillistvo"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    
<%
	request.setCharacterEncoding("UTF-8");

	String firstName = request.getParameter("firstName");
	String lastName = request.getParameter("lastName");
	String email = request.getParameter("email");
	
	Emaillistvo vo = new Emaillistvo();
	vo.setFirstName(firstName);
	vo.setLastName(lastName);
	vo.setEmail(email);
	
	new Emaillistdao().insert(vo);
	
	response.sendRedirect("/emaillist01");
%>