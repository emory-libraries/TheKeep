class Subject < ActiveRecord::Base
  belongs_to :Authority
  has_and_belongs_to_many :contents 
  
  
  def self.getSubjects
    @subjects = find(:all, :select => 'subject, id, authority_id', :order => 'subject')    
    
    sub = []    
    for subject in @subjects
      a = Authority.find(subject.authority_id)
      sub << [subject.subject + " [" + a.authority + "]", subject.id]
    end  
    
    return sub
  end  
end
