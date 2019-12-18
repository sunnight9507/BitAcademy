package dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import vo.EmaillistVo;

public class EmaillistDao {
	
	
	
	public List<EmaillistVo> findAll() {
		List<EmaillistVo> list = new ArrayList<>();
		
		Connection conn = null;
		Statement stmt = null;
		ResultSet rs = null;
		
		try {
			conn = getConnection();
			
			// 3. Statement 
			stmt = conn.createStatement();
			
			// 4. SQL문 실행
			String sql = "select no, first_name, last_name, email from table2";
			
			rs = stmt.executeQuery(sql);
			
			// 5. 결과 가져오기
			while(rs.next()) {
				Long no = rs.getLong(1);
				String firstName = rs.getString(2);
				String lastName = rs.getString(3);
				String email = rs.getString(4);
				
				EmaillistVo vo = new EmaillistVo();
				vo.setNo(no);
				vo.setFirstName(firstName);
				vo.setLastName(lastName);
				vo.setEmail(email);
				
				list.add(vo);
			}
			
		} catch (ClassNotFoundException e) {
			System.out.println("드라이버 로딩 실패:" + e);
		} catch (SQLException e) {
			System.out.println("error:" + e);
		} finally {
			try {
				//  6. 자원 정리 
				if(conn != null) {
					conn.close();
				}
				if(rs != null) {
					rs.close();
				}
				if(stmt != null) {
					stmt.close();
				}
				conn.close();
			} catch (SQLException e) {
				e.printStackTrace();
			}
		}
		return list;
	}
	
		
	public Boolean insert(EmaillistVo vo) {
		Boolean result = false;
		Connection conn = null;
		Statement stmt = null;
				
		try {
			conn = getConnection();
			
			// 3. Statement 
			stmt = conn.createStatement();
			
			// 4. SQL문 실행
			String sql = "insert into table2 values (null, '"+ vo.getFirstName() +"', '"+ vo.getLastName() +"', '"+ vo.getEmail() +"')";
			
			int count = stmt.executeUpdate(sql);
			
			result = count == 1;
			
		} catch (ClassNotFoundException e) {
			System.out.println("드라이버 로딩 실패:" + e);
		} catch (SQLException e) {
			System.out.println("error:" + e);
		} finally {
			try {
				//  6. 자원 정리 
				if(conn != null) {
					conn.close();
				}
				conn.close();
			} catch (SQLException e) {
				e.printStackTrace();
			}
		}
		
		return result;
	}
	
	private Connection getConnection() throws ClassNotFoundException, SQLException{
		// 1. JDBC Driver(Mysql) 로딩
		Class.forName("com.mysql.jdbc.Driver");
					
		// 2. 연결하기
		String url = "jdbc:mysql://localhost:3306/webdb";
		Connection conn = DriverManager.getConnection(url, "webdb", "webdb");
		
		return conn;
	}
}
