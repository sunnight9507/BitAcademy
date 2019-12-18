package dao.test;

import java.util.List;

import dao.EmaillistDao;
import vo.EmaillistVo;

public class EmaillistDaoTest {
	
	public static void main(String[] args) {
		insertTest();
		
		findAllTest();
	}
	
	public static void findAllTest() {
		List<EmaillistVo> list = new EmaillistDao().findAll();
		for(EmaillistVo vo : list) {
			System.out.println(vo);
		}
	}
	
	public static void insertTest() {
		EmaillistVo vo = new EmaillistVo();
		vo.setFirstName("안");
		vo.setLastName("대혁");
		vo.setEmail("keic@gmaail.com");
		
		EmaillistDao dao = new EmaillistDao();
		
		dao.insert(vo);
	}
}
