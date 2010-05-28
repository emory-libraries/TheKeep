class StaffName < ActiveRecord::Base
  has_one :Content
  
  
  def self.getStaff
    @staff = find(:all, :select => 'name, id')
    
    names = []    
    for s in @staff
      names << [s.name, s.id]
    end  
    
    return names
  end
end
