package com.cse03.backend.service.impl;

import com.cse03.backend.dto.request.RequestSignUp;
import com.cse03.backend.dto.response.ResponseSignUp;
import com.cse03.backend.entity.User;
import com.cse03.backend.entity.enums.LoginAuthProvider;
import com.cse03.backend.exception.DBException;
import com.cse03.backend.repository.UserRepository;
import com.cse03.backend.service.UserService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {

	private final UserRepository userRepository;

	public UserServiceImpl(UserRepository userRepository) {
		this.userRepository = userRepository;
	}

	@Override
	@Transactional
	public ResponseSignUp createUser(RequestSignUp requestSignUp) throws DBException {
		String name = requestSignUp.name();
		String email = requestSignUp.email();
		LoginAuthProvider loginAuthProvider = requestSignUp.loginAuthProvider();
		String username = requestSignUp.username();
		String password = requestSignUp.password();

		if (userRepository.findByEmail(email).isPresent()) {
			throw new DBException("user with email : " + email + " already exists ! ");
		}
		User user = User
			.builder()
			.name(name)
			.email(email)
			.username(username)
			.password(password)
			.loginAuthProvider(loginAuthProvider)
			.build();

		User save = userRepository.save(user);
		return new ResponseSignUp(
			save.getId(),
			save.getName(),
			save.getUsername(),
			save.getEmail(),
			save.getLoginAuthProvider()
		);
	}
}
