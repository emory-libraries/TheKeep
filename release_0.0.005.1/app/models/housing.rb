class Housing < ActiveRecord::Base
  has_many :SrcStillImage
  
  def self.getHousings
    @housings = find(:all, :select => 'description, id', :order => 'description')
    
    h = []    
    for housing in @housings
      h << [housing.description, housing.id]
    end  
    
    return h
  end  
end
