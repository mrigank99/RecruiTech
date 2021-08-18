$(document).ready(function()

    {
    var x = 0; //Initial field counter
    var list_maxField = 10; //Input fields increment limitation
    
        //Once add button is clicked
    $('.list_add_button').click(function()
        {
        //Check maximum number of input fields
        if(x < list_maxField){ 
            x++; //Increment field counter
            var list_fieldHTML = '<div class="mt-10"><div class="form-group"><input type="text" name="com_name" placeholder="Company Name" onfocus="this.placeholder = ''" class="single-input-primary"></div></div><div class="mt-10"><div class="form-group"><input type="date" name="com_from_date" placeholder="From" onfocus="this.placeholder = ''" class="single-input-primary"></div></div><div class="mt-10"><div class="form-group"><input type="date" name="com_to_date" placeholder="To" onfocus="this.placeholder = ''" class="single-input-primary"></div></div><div class="mt-10"><div class="form-group"><input type="text" name="designation" placeholder="Designation" onfocus="this.placeholder = ''" class="single-input-primary"></div></div><div class="mt-10"><div class="form-group"><input type="text" name="department" placeholder="Department" onfocus="this.placeholder = ''" class="single-input-primary"></div></div> <div class="mt-10"><div class="form-group"><textarea class="single-textarea" name = "about_role" placeholder="About the Role" onfocus="this.placeholder = ''" class="single-input-primary"></textarea></div></div><a href="javascript:void(0);" class="list_remove_button btn btn-danger">-</a>'; //New input field html
            $('.list_wrapper').append(list_fieldHTML); //Add field html
        }
        });
    
        //Once remove button is clicked
        $('.list_wrapper').on('click', '.list_remove_button', function()
        {
           $(this).closest('div.row').remove(); //Remove field html
           x--; //Decrement field counter
        });
});