package com.cse03.backend.service;


import com.cse03.backend.dto.request.RequestSignUp;
import com.cse03.backend.dto.response.ResponseSignUp;
import com.cse03.backend.entity.User;
import com.cse03.backend.exception.DBException;
import jakarta.transaction.Transactional;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.springframework.stereotype.Service;
import java.util.Optional ;


public interface UserService {

    @Transactional
    ResponseSignUp createUser(RequestSignUp requestSignUp ) throws DBException;

    Optional<User> findByEmail ( @NotNull @NotBlank String email );
}
