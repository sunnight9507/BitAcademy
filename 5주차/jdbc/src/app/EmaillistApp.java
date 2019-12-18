package app;

import java.util.List;
import java.util.Scanner;

import dao.EmaillistDao;
import vo.EmaillistVo;

public class EmaillistApp {
	public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);
		
		while(true) {
			System.out.println("입력>");
			String line = scanner.nextLine();
			
			if("quit".equals(line)) {
				break;
			}
			
			String[] tokens = line.split(" ");
			
			EmaillistVo vo = new EmaillistVo();
			vo.setFirstName(tokens[0]);
			vo.setLastName(tokens[1]);
			vo.setEmail(tokens[2]);
			
			EmaillistDao dao = new EmaillistDao();
			dao.insert(vo);
			
			System.out.println("=======Email List========");
			List<EmaillistVo> list = dao.findAll();
			for(EmaillistVo v : list) {
				System.out.println(v);
			}
			System.out.println("======================");
		}
		
		scanner.close();
	}
}
