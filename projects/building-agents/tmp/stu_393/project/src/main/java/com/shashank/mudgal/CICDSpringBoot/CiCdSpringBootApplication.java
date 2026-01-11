package com.shashank.mudgal.CICDSpringBoot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CiCdSpringBootApplication {

	public static void main(String[] args) {
		System.out.println("Hello Spring boot");
		SpringApplication.run(CiCdSpringBootApplication.class, args);
	}

}
