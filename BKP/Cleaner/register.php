<?php
/**
 * Template Name: Register Page
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
        <h1 class="display-4 text-white animated slideInDown mb-4">Register Today</h1>
        <nav aria-label="breadcrumb animated slideInDown">
            <ol class="breadcrumb justify-content-center mb-0">
                <li class="breadcrumb-item"><a class="text-white" href="<?php echo home_url('/'); ?>">Home</a></li>
                <li class="breadcrumb-item"><a class="text-white" href="#">Pages</a></li>
                <li class="breadcrumb-item text-primary active" aria-current="page">Register</li>
            </ol>
        </nav>
    </div>
</div>
<!-- Page Header End -->

<!-- Register Start -->
<div class="container-xxl py-5">
    <div class="container">
        <div class="row g-5">
            <div class="col-lg-6 wow fadeInUp" data-wow-delay="0.1s">
                <div class="position-relative overflow-hidden ps-5 pt-5 h-100" style="min-height: 400px;">
                    <img class="position-absolute w-100 h-100" src="<?php echo get_template_directory_uri(); ?>/assets/img/feature.jpg" alt="" style="object-fit: cover;">
                    <div class="position-absolute top-0 start-0 bg-white pe-3 pb-3" style="width: 200px; height: 200px;">
                        <div class="d-flex flex-column justify-content-center text-center bg-primary h-100 p-3">
                            <h1 class="text-white">Hey</h1>
                            <h2 class="text-white">Be A</h2>
                            <h5 class="text-white mb-0">Member</h5>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-6 wow fadeInUp" data-wow-delay="0.5s">
                <div class="h-100">
                    <div class="border-start border-5 border-primary ps-4 mb-5">
                        <h6 class="text-body text-uppercase mb-2">Hello there</h6>
                        <h1 class="display-6 mb-0">Become a member to get discounted deals</h1>
                    </div>
                    
                    <!-- Show errors/success -->
                    <?php if (isset($_GET['error'])): ?>
                        <div class="alert alert-danger">
                            <?php 
                            switch ($_GET['error']) {
                                case 'empty': echo 'Please fill all fields.'; break;
                                case 'username_exists': echo 'Username already exists.'; break;
                                case 'email_exists': echo 'Email already registered.'; break;
                                case 'password_mismatch': echo 'Passwords do not match.'; break;
                                default: echo 'Registration failed. Please try again.';
                            }
                            ?>
                        </div>
                    <?php endif; ?>
                    
                    <!-- Registration Form -->
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                        <input type="hidden" name="action" value="tf_register_user">
                        
                        <div class="row g-3">
                            <div class="col-md-6">
                                <div class="form-floating">
                                    <input type="text" class="form-control border-0 bg-light" id="username" name="username" placeholder="Username" required>
                                    <label for="username">Username *</label>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-floating">
                                    <input type="email" class="form-control border-0 bg-light" id="email" name="email" placeholder="Your Email" required>
                                    <label for="email">Your Email *</label>
                                </div>
                            </div>
                            <div class="col-12">
                                <div class="form-floating">
                                    <input type="password" class="form-control border-0 bg-light" id="password" name="password" placeholder="Password" required>
                                    <label for="password">Password *</label>
                                </div>
                            </div>
                            <div class="col-12">
                                <div class="form-floating">
                                    <input type="password" class="form-control border-0 bg-light" id="confirm_password" name="confirm_password" placeholder="Confirm Password" required>
                                    <label for="confirm_password">Confirm Password *</label>
                                </div>
                            </div>
                            <div class="col-12">
                                <div class="form-floating">
                                    <input type="text" class="form-control border-0 bg-light" id="phone" name="phone" placeholder="Phone Number">
                                    <label for="phone">Phone Number (Optional)</label>
                                </div>
                            </div>
                            <div class="col-12">
                                <div class="form-check">
                                    <input type="checkbox" class="form-check-input" id="terms" name="terms" required>
                                    <label class="form-check-label" for="terms">
                                        I agree to the <a href="<?php echo home_url('/terms'); ?>">Terms & Conditions</a> *
                                    </label>
                                </div>
                            </div>
                            <div class="col-12">
                                <button class="btn btn-primary py-3 px-5" type="submit">Register</button>
                            </div>
                        </div>
                    </form>
                    
                    <div class="mt-4 text-center">
                        <p>Already have an account? 
                            <a href="<?php echo home_url('/login'); ?>">Login here</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Register End -->

<?php get_footer(); ?>