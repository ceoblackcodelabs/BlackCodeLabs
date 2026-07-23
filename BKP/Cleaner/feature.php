<?php
/**
 * Template Name: Features Page
 * Template Post Type: page
 */
get_header();
?>
<!-- Page Header Start -->
<div class="container-fluid page-header py-5 mb-5 wow fadeIn" data-wow-delay="0.1s">
    <div class="container text-center py-5">
        <h1 class="display-4 text-white animated slideInDown mb-4">Features</h1>
        <nav aria-label="breadcrumb animated slideInDown">
            <ol class="breadcrumb justify-content-center mb-0">
                <li class="breadcrumb-item"><a class="text-white" href="#">Home</a></li>
                <li class="breadcrumb-item"><a class="text-white" href="#">Pages</a></li>
                <li class="breadcrumb-item text-primary active" aria-current="page">Features</li>
            </ol>
        </nav>
    </div>
</div>
<!-- Page Header End -->

<!-- Features Start -->
<div class="container-xxl py-5">
    <div class="container">
        <div class="row g-5">
            <div class="col-lg-6 wow fadeInUp" data-wow-delay="0.1s">
                <div class="border-start border-5 border-primary ps-4 mb-5">
                    <h6 class="text-body text-uppercase mb-2">Why Choose Us!</h6>
                    <h1 class="display-6 mb-0">Our Specialization And Company Features</h1>
                </div>

                <p class="mb-5">
                    We deliver reliable and professional cleaning and hygiene services for residential, commercial, and industrial clients.
                    Our experienced team uses modern equipment and environmentally friendly products to ensure clean, safe, and healthy spaces every time.
                </p>

                <div class="row gy-5 gx-4">
                    <div class="col-sm-6 wow fadeIn" data-wow-delay="0.1s">
                        <div class="d-flex align-items-center mb-3">
                            <i class="fa fa-check fa-2x text-primary flex-shrink-0 me-3"></i>
                            <h6 class="mb-0">Wide Range of Services</h6>
                        </div>
                        <span>
                            We offer comprehensive cleaning solutions including office, residential, post-construction, pest control, waste management, and landscaping services.
                        </span>
                    </div>

                    <div class="col-sm-6 wow fadeIn" data-wow-delay="0.2s">
                        <div class="d-flex align-items-center mb-3">
                            <i class="fa fa-check fa-2x text-primary flex-shrink-0 me-3"></i>
                            <h6 class="mb-0">5+ Years of Experience</h6>
                        </div>
                        <span>
                            Our team brings over five years of professional experience, ensuring efficient service delivery and consistent quality standards.
                        </span>
                    </div>

                    <div class="col-sm-6 wow fadeIn" data-wow-delay="0.3s">
                        <div class="d-flex align-items-center mb-3">
                            <i class="fa fa-check fa-2x text-primary flex-shrink-0 me-3"></i>
                            <h6 class="mb-0">Trusted by Many Clients</h6>
                        </div>
                        <span>
                            We have earned the trust of homeowners, offices, and industrial clients through reliability, professionalism, and attention to detail.
                        </span>
                    </div>

                    <div class="col-sm-6 wow fadeIn" data-wow-delay="0.4s">
                        <div class="d-flex align-items-center mb-3">
                            <i class="fa fa-check fa-2x text-primary flex-shrink-0 me-3"></i>
                            <h6 class="mb-0">Affordable & Reliable Pricing</h6>
                        </div>
                        <span>
                            Our pricing is transparent and competitive, delivering excellent value without compromising on quality or service standards.
                        </span>
                    </div>
                </div>
            </div>

            <div class="col-lg-6 wow fadeInUp" data-wow-delay="0.5s">
                <div class="position-relative overflow-hidden ps-5 pt-5 h-100" style="min-height: 400px;">
                    <img class="position-absolute w-100 h-100" src="img/feature.jpg" alt="" style="object-fit: cover;">
                    <div class="position-absolute top-0 start-0 bg-white pe-3 pb-3" style="width: 200px; height: 200px;">
                        <div class="d-flex flex-column justify-content-center text-center bg-primary h-100 p-3">
                            <h1 class="text-white">5+</h1>
                            <h2 class="text-white">Years</h2>
                            <h5 class="text-white mb-0">Proven Excellence</h5>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Features End -->

<!-- Testimonial Start -->
<div class="container-xxl py-5">
    <div class="container">
        <div class="row g-5">
            <div class="col-lg-5 wow fadeInUp" data-wow-delay="0.1s">
                <div class="border-start border-5 border-primary ps-4 mb-5">
                    <h6 class="text-body text-uppercase mb-2">Testimonial</h6>
                    <h1 class="display-6 mb-0">What Our Clients Say</h1>
                </div>
                <p class="mb-4">
                    We are trusted by homeowners, businesses, and industries for delivering reliable and high-quality cleaning services.
                </p>

                <div class="row g-4">
                    <div class="col-sm-6">
                        <div class="d-flex align-items-center mb-2">
                            <i class="fa fa-users fa-2x text-primary flex-shrink-0"></i>
                            <h1 class="ms-3 mb-0">250+</h1>
                        </div>
                        <h5 class="mb-0">Satisfied Clients</h5>
                    </div>

                    <div class="col-sm-6">
                        <div class="d-flex align-items-center mb-2">
                            <i class="fa fa-check fa-2x text-primary flex-shrink-0"></i>
                            <h1 class="ms-3 mb-0">400+</h1>
                        </div>
                        <h5 class="mb-0">Projects Completed</h5>
                    </div>
                </div>
            </div>

            <div class="col-lg-7 wow fadeInUp" data-wow-delay="0.5s">
                <div class="owl-carousel testimonial-carousel">
                    <div class="testimonial-item">
                        <img class="img-fluid mb-4" src="<?php echo get_template_directory_uri(); ?>/assets/img/testimonial-1.jpg" alt="Mary Jones">
                        <p class="fs-5">
                            The team was professional, punctual, and extremely thorough. Our space looks brand new.
                        </p>
                        <div class="bg-primary mb-3" style="width: 60px; height: 5px"></div>
                        <h5>Mary Jones</h5>
                        <span>Business Owner</span>
                    </div>

                    <div class="testimonial-item">
                        <img class="img-fluid mb-4" src="<?php echo get_template_directory_uri(); ?>/assets/img/testimonial-2.jpg" alt="Ann Njoki">
                        <p class="fs-5">
                            Excellent service and attention to detail. Highly recommended for both home and office cleaning.
                        </p>
                        <div class="bg-primary mb-3" style="width: 60px; height: 5px"></div>
                        <h5>Ann Njoki</h5>
                        <span>Homeowner</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Testimonial End -->

<?php get_footer(); ?>

