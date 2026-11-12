package com.cse03.backend.service.impl;

import com.cse03.backend.dto.request.RequestSignUp;
import com.cse03.backend.dto.response.ResponseSignUp;
import com.cse03.backend.entity.User;
import com.cse03.backend.entity.enums.LoginAuthProvider;
import com.cse03.backend.exception.DBException;
import com.cse03.backend.repository.UserRepository;
import com.cse03.backend.service.UserService;
import jakarta.transaction.Transactional;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(12);

    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    @Transactional
    public ResponseSignUp createUser(RequestSignUp requestSignUp) throws DBException {
        String email = requestSignUp.email();
        if (userRepository.findByEmail(email).isPresent()) {
            throw new DBException("exist with email : " + email);
        }

        LoginAuthProvider provider = requestSignUp.loginAuthProvider();
        User user = User.builder()
                .name(requestSignUp.name())
                .email(email)
                .username(requestSignUp.username())
                .password(provider == LoginAuthProvider.GOOGLE
                        ? null
                        : encoder.encode(requestSignUp.password()))
                .loginAuthProvider(provider)
                .build();

        User saved = userRepository.save(user);
        return new ResponseSignUp(
                saved.getId(),
                saved.getName(),
                saved.getUsername(),
                saved.getEmail(),
                saved.getLoginAuthProvider()
        );
    }

    @Override
    public Optional<User> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }
}
