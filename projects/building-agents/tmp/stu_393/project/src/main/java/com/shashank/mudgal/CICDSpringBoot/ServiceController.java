package com.shashank.mudgal.CICDSpringBoot;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ServiceController {
	
	@GetMapping("/hello")
	public String method1() {
		return "Welcome Shashank";
	}
}
