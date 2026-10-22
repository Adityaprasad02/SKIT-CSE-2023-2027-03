package com.cse03.backend.entity;


import com.cse03.backend.entity.enums.LoginAuthProvider;
import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.*;
import org.jspecify.annotations.Nullable;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.List;
import java.util.UUID;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "app_users")
@Builder
public class User implements UserDetails {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id  ;

    @Column(name = "name" , unique = false , nullable = false)
    @NotBlank(message = "name is required")
    private String name ;

    @Column(name = "username" , unique = true , nullable = false)
    private String username ;


    @Column(name = "email" , unique = true , nullable = false)
    @NotBlank(message = "email is required")
    @Email
    private String email ;


    @Column(name = "password" , nullable = true)
    private String password ;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false , name = "auth")
    private LoginAuthProvider loginAuthProvider ;


    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of();
    }
}
