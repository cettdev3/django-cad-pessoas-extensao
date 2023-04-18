
$('.custom-image-thumbnail img').each(function () {
    galleryImages.push($(this).attr('src'));
});
var currentImageIndex = 0;

$('body').on('click', '.custom-image-thumbnail', function () {
    if ($(event.target).hasClass('custom-remove-img-button') || $(event.target).parents('.custom-remove-img-button').length > 0) {
        return;
    }
    currentImageIndex = $(this).index('.custom-image-thumbnail');
    var imageSrc = $(this).find('img').attr('src');
    $('.custom-img-modal').show();
    $('.custom-img-modal-content img').attr('src', imageSrc);
});

$('body').on('click','.custom-img-modal', function () {

    $('.custom-img-modal').hide();
});

$('body').on('click', '.custom-img-modal-content', function (event) {

    event.stopPropagation();
});

$('body').on('click','.nav-button-container', function (event) {
    event.stopPropagation();
});

$('body').on('click','.nav-button-container.left', function () {
    currentImageIndex = (currentImageIndex === 0) ? galleryImages.length - 1 : currentImageIndex - 1;
    $('.custom-img-modal-content img').attr('src', galleryImages[currentImageIndex]);
});

$('body').on('click','.nav-button-container.right', function () {
    currentImageIndex = (currentImageIndex === galleryImages.length - 1) ? 0 : currentImageIndex + 1;

    $('.custom-img-modal-content img').attr('src', galleryImages[currentImageIndex]);
});

$('body').on('click','.custom-img-modal-close', function () {

    $('.custom-img-modal').hide();
});