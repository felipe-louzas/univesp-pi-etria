Inputmask.extendDefinitions({
    'X': {
        validator: "[xX]",
        casing: "upper" //auto uppercasing
    },
});
Inputmask.extendAliases({
    'phone': {
        mask: ['(99) 9999-9999', '(99) 99999-9999'],
    },
    'cpf': {
        mask: '999.999.999-99',
    },
    'rg': {
        mask: '99.999.999-9|X',
    },
    'cep': {
        mask: '99999-999',
    },
    'date': {
        mask: '99/99/9999',
    },
    datehourminute: {
        mask: '99/99/9999 99:99',
    },
});

$(document).ready(function () {
    $(".image-upload").on('change', function () {

        if (typeof (FileReader) != "undefined") {

            const image_holder = $(this).closest('.image-upload-control').find('.image-holder');

            image_holder.empty();

            var reader = new FileReader();
            reader.onload = function (e) {
                $("<img />", {
                    "src": e.target.result,
                    "class": "w-100 object-fit-contain"
                }).appendTo(image_holder);

            }
            image_holder.show();
            reader.readAsDataURL($(this)[0].files[0]);
        } 
    });


    $('.btn-doc-modal').on('click', function () {
        const docUrl = $(this).data('doc-url');
        const target = $(this).data('bs-target');
        $(target).find('.modal-body').html('<img src="' + docUrl + '" class="w-100 object-fit-contain" />');
    });

});
