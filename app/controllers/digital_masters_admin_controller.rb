class DigitalMastersAdminController < ApplicationController
  def index
  end
  
  #####################################################################################################
  #authority controls
  #####################################################################################################    
  def authority_list
    @authority_pages, @authorities = paginate :authorities, :per_page => 10, :order => 'authority'
  end

  def authority_show
    @authority = Authority.find(params[:id])
  end

  def authority_new
    @authority = Authority.new
  end

  def authority_create
    @authority = Authority.new(params[:authority])
    if @authority.save
      flash[:notice] = 'Authority was successfully created.'
      redirect_to :action => 'authority_list'
    else
      render :action => 'authority_new'
    end
  end

  def authority_edit
    @authority = Authority.find(params[:id])
  end

  def authority_update
    @authority = Authority.find(params[:id])
    if @authority.update_attributes(params[:authority])
      flash[:notice] = 'Authority was successfully updated.'
      redirect_to :action => 'authority_show', :id => @authority
    else
      render :action => 'authority_edit'
    end
  end

  def authority_destroy
    Authority.find(params[:id]).destroy
    redirect_to :action => 'authority_list'
  end
  
  
  #####################################################################################################
  #Name controls
  #####################################################################################################  
  # GETs should be safe (see http://www.w3.org/2001/tag/doc/whenToUseGet.html)
  verify :method => :post, :only => [ :name_destroy, :name_create, :name_update ],
         :redirect_to => { :action => :name_list }
           
  def name
    name_list
    render :action => 'name_list'
  end

  # GETs should be safe (see http://www.w3.org/2001/tag/doc/whenToUseGet.html)
  verify :method => :post, :only => [ :destroy, :create, :update ],
         :redirect_to => { :action => :list }

  def name_list
    @name_pages, @names = paginate :names, :per_page => 100, :order => 'name'
  end

  def name_show
    @name = Name.find(params[:id])
  end

  def name_new
    @name = Name.new
  end

  def name_create
    @name = Name.new(params[:name])
    if @name.save
      flash[:notice] = 'Name was successfully created.'
      redirect_to :action => 'name_list'
    else
      render :action => 'name_new'
    end
  end

  def name_edit
    @name = Name.find(params[:id])
  end

  def name_update
    @name = Name.find(params[:id])
    if @name.update_attributes(params[:name])
      flash[:notice] = 'Name was successfully updated.'
      redirect_to :action => 'name_show', :id => @name
    else
      render :action => 'name_edit'
    end
  end

  def name_destroy
    Name.find(params[:id]).destroy
    redirect_to :action => 'name_list'
  end
  
  #####################################################################################################  
  #Subject Controls
  #####################################################################################################
  # GETs should be safe (see http://www.w3.org/2001/tag/doc/whenToUseGet.html)
  verify :method => :post, :only => [ :subject_destroy, :subject_create, :subject_update ],
         :redirect_to => { :action => :subject_list }
           
  def subject
    subject_list
    render :action => 'subject_list'
  end

  def subject_list
    @subject_pages, @subjects = paginate :subjects, :per_page => 100, :order => 'subject'
  end

  def subject_show
    @subject = Subject.find(params[:id])
  end

  def subject_new
    @subject = Subject.new
  end

  def subject_create
    @subject = Subject.new(params[:subject])
    if @subject.save
      flash[:notice] = 'Subject was successfully created.'
      redirect_to :action => 'subject_list'
    else
      render :action => 'subject_new'
    end
  end

  def subject_edit
    @subject = Subject.find(params[:id])
  end

  def subject_update
    @subject = Subject.find(params[:id])
    if @subject.update_attributes(params[:subject])
      flash[:notice] = 'Subject was successfully updated.'
      redirect_to :action => 'subject_show', :id => @subject
    else
      render :action => 'subject_edit'
    end
  end

  def subject_destroy
    Subject.find(params[:id]).destroy
    redirect_to :action => 'subject_list'
  end  

  #####################################################################################################
  #Genre controls
  #####################################################################################################   
  # GETs should be safe (see http://www.w3.org/2001/tag/doc/whenToUseGet.html)
  verify :method => :post, :only => [ :genre_destroy, :genre_create, :genre_update ],
         :redirect_to => { :action => :genre_list }

  def genre_list
    @genre_pages, @genres = paginate :genres, :per_page => 100, :order => 'genre'
  end

  def genre_show
    @genre = Genre.find(params[:id])
  end

  def genre_new
    @genre = Genre.new
  end

  def genre_create
    @genre = Genre.new(params[:genre])
    if @genre.save
      flash[:notice] = 'Genre was successfully created.'
      redirect_to :action => 'genre_list'
    else
      render :action => 'genre_new'
    end
  end

  def genre_edit
    @genre = Genre.find(params[:id])
  end

  def genre_update
    @genre = Genre.find(params[:id])
    if @genre.update_attributes(params[:genre])
      flash[:notice] = 'Genre was successfully updated.'
      redirect_to :action => 'genre_show', :id => @genre
    else
      render :action => 'genre_edit'
    end
  end

  def genre_destroy
    Genre.find(params[:id]).destroy
    redirect_to :action => 'genre_list'
  end  

  #####################################################################################################
  #Restriction controls
  #####################################################################################################    
  def restriction_list
    @restriction_pages, @restrictions = paginate :restrictions, :per_page => 100, :order => 'description'
  end

  def restriction_show
    @restriction = Restriction.find(params[:id])
  end

  def restriction_new
    @restriction = Restriction.new
  end

  def restriction_create
    @restriction = Restriction.new(params[:restriction])
    if @restriction.save
      flash[:notice] = 'Restriction was successfully created.'
      redirect_to :action => 'restriction_list'
    else
      render :action => 'restriction_new'
    end
  end

  def restriction_edit
    @restriction = Restriction.find(params[:id])
  end

  def restriction_update
    @restriction = Restriction.find(params[:id])
    if @restriction.update_attributes(params[:restriction])
      flash[:notice] = 'Restriction was successfully updated.'
      redirect_to :action => 'restriction_show', :id => @restriction
    else
      render :action => 'restriction_edit'
    end
  end

  def restriction_destroy
    Restriction.find(params[:id]).destroy
    redirect_to :action => 'restriction_list'
  end  
  
  #####################################################################################################
  #Staff controls
  #####################################################################################################      
  def staff_list
    @staff_name_pages, @staff_names = paginate :staff_names, :per_page => 10, :order => 'name'
  end

  def staff_show
    @staff_name = StaffName.find(params[:id])
  end

  def staff_new
    @staff_name = StaffName.new
  end

  def staff_create
    @staff_name = StaffName.new(params[:staff_name])
    if @staff_name.save
      flash[:notice] = 'StaffName was successfully created.'
      redirect_to :action => 'staff_list'
    else
      render :action => 'staff_new'
    end
  end

  def staff_edit
    @staff_name = StaffName.find(params[:id])
  end

  def staff_update
    @staff_name = StaffName.find(params[:id])
    if @staff_name.update_attributes(params[:staff_name])
      flash[:notice] = 'Staff was successfully updated.'
      redirect_to :action => 'staff_show', :id => @staff_name
    else
      render :action => 'staff_edit'
    end
  end

  def staff_destroy
    StaffName.find(params[:id]).destroy
    redirect_to :action => 'staff_list'
  end  


  #####################################################################################################
  #Role controls
  #####################################################################################################     
  def role_list
    @role_pages, @roles = paginate :roles, :per_page => 100
  end

  def role_show
    @role = Role.find(params[:id])
  end

  def role_new
    @role = Role.new
  end

  def role_create
    @role = Role.new(params[:role])
    if @role.save
      flash[:notice] = 'Role was successfully created.'
      redirect_to :action => 'role_list'
    else
      render :action => 'role_new'
    end
  end

  def role_edit
    @role = Role.find(params[:id])
  end

  def role_update
    @role = Role.find(params[:id])
    if @role.update_attributes(params[:role])
      flash[:notice] = 'Role was successfully updated.'
      redirect_to :action => 'role_show', :id => @role
    else
      render :action => 'role_edit'
    end
  end

  def role_destroy
    Role.find(params[:id]).destroy
    redirect_to :action => 'role_list'
  end
  
  def fixDatabase()
    ManuscriptAccession::fixDatabase
    flash[:notice] = 'Database has been repaired'
    
    redirect_to :action => 'index'
  end
  
end
