package com.cse03.backend.config;


import com.cse03.backend.service.impl.CustomUserDetailService;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.annotation.web.configurers.HeadersConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.List;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    private final CustomUserDetailService customUserDetailService ;


    public SecurityConfig(CustomUserDetailService customUserDetailService) {
        this.customUserDetailService = customUserDetailService;

    }


    @Bean
    public SecurityFilterChain securityFilterChain ( HttpSecurity httpSecurity ) {
        httpSecurity.csrf ( AbstractHttpConfigurer :: disable )
                .headers ( headers -> headers.frameOptions ( HeadersConfigurer.FrameOptionsConfig :: sameOrigin ) )
                .authorizeHttpRequests ( (
                        request ) ->
                        request.requestMatchers (
                                        "/login/**" , "/signup/**" , "/h2-console/**" , "/logout/" , "/api/v1/health"
                                ).permitAll ( )
                                .anyRequest ( ).authenticated ( )
                )
                .sessionManagement ( session
                        -> session.sessionCreationPolicy ( SessionCreationPolicy.STATELESS ) )
                .cors ( Customizer.withDefaults ( ) )
                .authenticationProvider ( authProvider ( ) )
                .exceptionHandling ( ex -> ex
                        .authenticationEntryPoint ( ( request , response
                                , authException ) -> {
                            response.setContentType ( "application/json" );
                            response.setStatus ( HttpServletResponse.SC_UNAUTHORIZED );
                            response.getWriter ( ).write ( "{\"error\":\"Unauthorized\",\"message\":\"" + authException.getMessage ( ) + "\"}" );
                        } ) )
                .logout ( AbstractHttpConfigurer :: disable );


        return httpSecurity.build ( );
    }

    @Bean
    public AuthenticationProvider authProvider() {
        DaoAuthenticationProvider daoAuthenticationProvider
                = new DaoAuthenticationProvider(customUserDetailService) ;
        daoAuthenticationProvider.setPasswordEncoder(new BCryptPasswordEncoder(12));
        return daoAuthenticationProvider ;
    }

    @Bean
    public AuthenticationManager authenticationManager (AuthenticationConfiguration authenticationConfiguration) {
          return authenticationConfiguration.getAuthenticationManager() ;
    }


    @Bean
    public CorsConfigurationSource corsConfigurationSource(
    ) {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        configuration.setAllowedHeaders(List.of("Authorization", "Content-Type", "X-Requested-With" , "X-REFRESH-TOKEN"));
        configuration.setExposedHeaders(List.of("Authorization"));
        configuration.setAllowCredentials(true);
        configuration.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}
