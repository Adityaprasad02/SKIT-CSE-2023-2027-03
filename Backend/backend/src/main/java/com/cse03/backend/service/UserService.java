package com.cse03.backend.service;


import com.cse03.backend.dto.request.RequestSignUp;
import com.cse03.backend.dto.response.ResponseSignUp;
import com.cse03.backend.exception.DBException;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;


public interface UserService {

    @Transactional
    ResponseSignUp createUser(RequestSignUp requestSignUp ) throws DBException;

}
