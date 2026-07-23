<?php
/**
 * Template Name: Login Page
 * Template Post Type: page
 */

// If already logged in, redirect to home
if (is_user_logged_in()) {
    wp_redirect(home_url('/'));
    exit;
}

get_header();
?>

<!-- Page Header Start -->
<div class="container-fluid page-header py-5 mb-5 wow fadeIn" data-wow-delay="0.1s">
    <div class="container text-center py-5">
        <h1 class="display-4 text-white animated slideInDown mb-4">Login Today</h1>
        <nav aria-label="breadcrumb animated slideInDown">
            <ol class="breadcrumb justify-content-center mb-0">
                <li class="breadcrumb-item"><a class="text-white" href="<?php echo home_url('/login'); ?>">Login</a></li>
                <li class="breadcrumb-item"><a class="text-white" href="<?php echo home_url('/register'); ?>">Register</a></li>
            </ol>
        </nav>
    </div>
</div>
<!-- Page Header End -->

<!-- Login Start -->
<div class="container-xxl py-5">
    <div class="container">
        <div class="row g-5">
            <div class="col-lg-6 wow fadeInUp" data-wow-delay="0.1s">
                <div class="position-relative overflow-hidden ps-5 pt-5 h-100" style="min-height: 400px;">
                    <img class="position-absolute w-100 h-100" src="<?php echo get_template_directory_uri(); ?>/assets/img/feature.jpg" alt="" style="object-fit: cover;">
                    <div class="position-absolute top-0 start-0 bg-white pe-3 pb-3" style="width: 200px; height: 200px;">
                        <div class="d-flex flex-column justify-content-center text-center bg-primary h-100 p-3">
                            <h1 class="text-white">Hey</h1>
                            <h2 class="text-white">Welcome</h2>
                            <h5 class="text-white mb-0">Back</h5>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-6 wow fadeInUp" data-wow-delay="0.5s">
                <div class="h-100">
                    <div class="border-start border-5 border-primary ps-4 mb-5">
                        <h6 class="text-body text-uppercase mb-2">Hello There</h6>
                        <h1 class="display-6 mb-0">Login To Proceed</h1>
                    </div>
                    
                    <!-- Display login status messages -->
                    <?php
                    // Check for URL parameters to show messages
                    if (isset($_GET['error'])) {
                        $error = $_GET['error'];
                        echo '<div class="alert alert-danger alert-dismissible fade show">';
                        echo '<strong>Login Error:</strong> ';
                        
                        switch ($error) {
                            case 'invalid_credentials':
                                echo 'Invalid username or password. Please try again.';
                                break;
                            case 'empty_fields':
                                echo 'Please fill in both username and password fields.';
                                break;
                            default:
                                echo 'An error occurred during login. Please try again.';
                        }
                        
                        echo '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
                        echo '</div>';
                    }
                    
                    if (isset($_GET['registration']) && $_GET['registration'] == 'success') {
                        echo '<div class="alert alert-success alert-dismissible fade show">';
                        echo '<strong>Success!</strong> Registration successful! You can now login with your credentials.';
                        echo '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
                        echo '</div>';
                    }
                    
                    if (isset($_GET['logged_out']) && $_GET['logged_out'] == '1') {
                        echo '<div class="alert alert-success alert-dismissible fade show">';
                        echo '<strong>Success!</strong> You have been successfully logged out.';
                        echo '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
                        echo '</div>';
                    }
                    ?>
                    
                    <!-- Login Form -->
                    <form name="loginform" id="loginform" action="<?php echo esc_url(site_url('wp-login.php', 'login_post')); ?>" method="post">
                        <div class="mb-3">
                            <label for="user_login" class="form-label">Username or Email *</label>
                            <input type="text" name="log" id="user_login" class="form-control border-0 bg-light px-4" value="" size="20" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="user_pass" class="form-label">Password *</label>
                            <input type="password" name="pwd" id="user_pass" class="form-control border-0 bg-light px-4" value="" size="20" required>
                        </div>
                        
                        <div class="mb-3 form-check">
                            <input type="checkbox" name="rememberme" id="rememberme" class="form-check-input" value="forever">
                            <label for="rememberme" class="form-check-label">Remember Me</label>
                        </div>
                        
                        <!-- Hidden fields for redirect -->
                        <input type="hidden" name="redirect_to" value="<?php echo home_url('/'); ?>">
                        <input type="hidden" name="testcookie" value="1">
                        
                        <div class="mb-3">
                            <button type="submit" name="wp-submit" id="wp-submit" class="btn btn-primary py-3 px-5 w-100">
                                <i class="fas fa-sign-in-alt me-2"></i>Login
                            </button>
                        </div>
                        
                        <div class="text-center">
                            <p class="mb-2">
                                <a href="<?php echo wp_lostpassword_url(home_url('/login')); ?>">
                                    <i class="fas fa-key me-1"></i>Forgot Password?
                                </a>
                            </p>
                            <p class="mb-0">
                                Don't have an account? 
                                <a href="<?php echo home_url('/register'); ?>" class="fw-bold">
                                    <i class="fas fa-user-plus me-1"></i>Register here
                                </a>
                            </p>
                        </div>
                    </form>
                    
                    <!-- Debug info (remove in production) -->
                    <?php if (isset($_GET['debug'])): ?>
                    <div class="mt-4 p-3 bg-light border rounded">
                        <h6>Debug Info:</h6>
                        <p><strong>Login URL:</strong> <?php echo esc_url(site_url('wp-login.php', 'login_post')); ?></p>
                        <p><strong>Current User:</strong> <?php echo is_user_logged_in() ? 'Logged In' : 'Not Logged In'; ?></p>
                        <p><strong>GET Parameters:</strong> <?php echo json_encode($_GET); ?></p>
                    </div>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Login End -->

<?php get_footer(); ?>